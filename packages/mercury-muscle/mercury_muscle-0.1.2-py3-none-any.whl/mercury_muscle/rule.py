import re
import math
import numpy as np
import pandas as pd
from tqdm import tqdm
from copy import deepcopy
from tabulate import tabulate

from mercury_muscle.utils import increment
from mercury_muscle.score import MercuriTable


class RuleEvaluator:
    def __init__(
        self,
        mt: MercuriTable,
        target=None
    ) -> None:
        self.mt = mt
        self.target = target
        self.rules = []

        self.cm_patients = mt.df[["id", "disease"]].copy()
        self.totals_patients = mt.df[["id", "disease"]].copy()
        self.cm_patients.set_index("id", inplace=True)
        self.totals_patients.set_index("id", inplace=True)

        self.totals = None
        self.cm = None

    def add_rule(self, query, alias=None):
        self.rules.append(Rule(query, alias))
        col_name = alias if not alias == None else query
        self.cm_patients[col_name] = ""
        self.totals_patients[col_name] = ""

    def evaluate(self, side="R", mode="totals", sequential:bool = False):

        if mode=="cm":
            if self.target == None:
                raise Exception("RuleEvaluator target must be set")
            res_df = pd.DataFrame(columns=["tp", "fp", "tn", "fn", "nan"])

        elif mode=="totals":
            res_df = pd.DataFrame(columns=["rule", "true", "false", "nan"])

        if not side in ["L", "R"]:
            raise ValueError('side must be "R" or "L"')
        
        last_rule = None
        for r in self.rules:
            rule_name = r.alias if not r.alias == None else r.query

            self._evaluate(r.query, side, mode, rule_name, sequential, last_rule)

            if mode == "cm":
                unique = np.unique(list(self.cm_patients[rule_name]), return_counts=True)
            elif mode == "totals":
                unique = np.unique(list(self.totals_patients[rule_name]), return_counts=True)

            res = {k: [v] for k, v in zip(unique[0], unique[1])}
            res["rule"] = rule_name
            res_df = pd.concat([res_df, pd.DataFrame(res)], ignore_index=True)

            last_rule = rule_name

        setattr(self, mode, res_df.copy())

    def _evaluate(self, query, side, mode, rule_name, sequential,  last_rule):
        subsets = query.split('->')
        for i, sub in enumerate(subsets):
            labels = list(filter(None, re.split("[<>=()|&\d]", sub)))
            labels.sort(key=lambda s: len(s), reverse=True)
            if i == 0 : 
                population = deepcopy(self.mt.patients)
            else:
                population = deepcopy(population_tmp)

            population_tmp = []
            for p in population:
                nan_found = False
                query_subs = sub
                for l in labels:
                    score = getattr(p, f"muscles_{side}")[l].score
                    if np.isnan(score):
                        if mode=="cm": self.cm_patients.at[p.id, rule_name] = 'nan'
                        elif mode=="totals": self.totals_patients.at[p.id, rule_name] = 'nan'
                        nan_found = True
                        break
                    query_subs = query_subs.replace(l, str(score))

                query_subs = query_subs.replace("&", " and ").replace("|", " or ")
                last_sub = i == len(subsets) - 1
                if mode == 'totals': ev = self._evaluate_rule_totals
                elif mode == 'cm': ev = self._evaluate_rule_cm
                else: raise Exception(f'Unexpected mode: {mode}')
                population_tmp = ev(query_subs, last_sub, population_tmp, p, rule_name, nan_found, sequential, last_rule)

    def _evaluate_rule_totals(self, query_subs, last_sub, population_tmp, p, rule_name, nan_found, sequential, last_rule):
        if(
            sequential and 
            not last_rule == None and
            not self.totals_patients.at[p.id, last_rule] == 'true'
        ):
            self.totals_patients.at[p.id, rule_name] = 'ignore'
        elif nan_found:
            self.totals_patients.at[p.id, rule_name] = 'nan'
        elif eval(query_subs) == True:
            if not last_sub:
                population_tmp.append(p)
            else: 
                self.totals_patients.at[p.id, rule_name] = 'true'
        elif eval(query_subs) == False:
            if last_sub:
                self.totals_patients.at[p.id, rule_name] = 'false'
            else:
                self.totals_patients.at[p.id, rule_name] = 'ignore'
        else:
            raise Exception(
                f"The evaluated expression returned a value other than True or False: {query_subs}"
            )
        return population_tmp

    def _evaluate_rule_cm(self, query_subs, last_sub, population_tmp, p, rule_name, nan_found, sequential,  last_rule):
        positive = p.disease == self.target

        if(
            sequential and 
            not last_rule == None and
            not self.cm_patients.at[p.id, last_rule] == 'tp' and
            not self.cm_patients.at[p.id, last_rule] == 'fp'
        ):
            self.cm_patients.at[p.id, rule_name] = 'ignore'
        elif nan_found:
            self.cm_patients.at[p.id, rule_name] = 'nan'
        elif eval(query_subs) == True:
            if positive and not last_sub: 
                population_tmp.append(p)
            elif positive and last_sub: 
                self.cm_patients.at[p.id, rule_name] = 'tp'
            elif not positive and not last_sub:
                population_tmp.append(p)
            elif not positive and last_sub:
                self.cm_patients.at[p.id, rule_name] = 'fp'
        elif eval(query_subs) == False:
            if positive and last_sub: 
                self.cm_patients.at[p.id, rule_name] = 'fn'
            elif not positive and last_sub:
                self.cm_patients.at[p.id, rule_name] = 'tn'
            else:
                self.cm_patients.at[p.id, rule_name] = 'ignore'
        else:
            raise Exception(
                f"The evaluated expression returned a value other than True or False: {query_subs}"
            )
        return population_tmp
    
    def cm_stats(self):
        if not isinstance(self.cm, pd.DataFrame):
            print('The confussion matrix dataframe does not exist. Run evaluate_cm()')
            return

        res = {
            "Rule": [],
            "Accuracy": [],
            "Sensitivity": [],
            "Specificity": [],
            "PPV": [],
            "NPV": [],
            "F1-Score": [],
            "MCC": [],
            "normMCC": [],
            "DOR": [],
            "Population": [],
            "Positives": [],
            "Negatives": [],
        }
        for idx, row in self.cm.iterrows():
            tp = row["tp"]
            fp = row["fp"]
            tn = row["tn"]
            fn = row["fn"]

            t = tp + tn + fp + fn

            accuracy = (tp + tn) / (t)
            sensitivity = tp / (tp + fn)
            specificity = tn / (tn + fp)
            ppv = tp / (tp + fp)
            npv = tn / (tn + fn)
            f1_score = (2 * tp) / ((2 * tp) + fp + fn)
            mcc = ((tp * tn) - (fp * fn)) / math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
            norm_mcc = (mcc + 1) / 2
            dor = ((tp + 0.5) * (tn + 0.5)) / ((fp + 0.5) * (fn + 0.5))
            pos = (tp + fn) / t
            neg = (tn + fp) / t

            res["Rule"].append(row["rule"])
            res["Accuracy"].append(accuracy)
            res["Sensitivity"].append(sensitivity)
            res["Specificity"].append(specificity)
            res["PPV"].append(ppv)
            res["NPV"].append(npv)
            res["F1-Score"].append(f1_score)
            res["MCC"].append(mcc)
            res["normMCC"].append(norm_mcc)
            res["DOR"].append(dor)
            res["Population"].append(t)
            res["Positives"].append(pos)
            res["Negatives"].append(neg)

        return pd.DataFrame(res)

    def show_rules(self) -> pd.DataFrame:
        res = {
            "Alias": [r.alias for r in self.rules],
            "Query": [r.query for r in self.rules]
        }
        return pd.DataFrame(res)
    
    def show_totals(self):
        if isinstance(self.totals, pd.DataFrame):
            print(tabulate(self.totals, headers="keys", tablefmt="github"))
        else:
            print("Totals not evaluated, run evaluate_totals()")

    def show_cm(self):
        if isinstance(self.cm, pd.DataFrame):
            print(tabulate(self.cm, headers="keys", tablefmt="github"))
        else:
            print("Confussion Matrixes not evaluated, run evaluate_cm()")
    
    def update_rule(self, idx, alias=None, query=None):
        old_col_name = r.alias if not r.alias == None else r.query

        if not alias == None: self.rules[idx].alias = alias
        if not query == None: self.rules[idx].query = query

        r = self.rules[idx]
        new_col_name = r.alias if not r.alias == None else r.query
        self.cm_patients.rename({old_col_name: new_col_name})
        self.totals_patients.rename({old_col_name: new_col_name})

class Rule:
    def __init__(self, query: str, alias: str = None) -> None:
        self.query = query
        self.alias = alias
