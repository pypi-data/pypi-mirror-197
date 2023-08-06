import re
import warnings
import numpy as np
import pandas as pd

"""Object containing the Mercuri data, expects a table with the format:

| id  | disease | muscle1_L | muscle1_R | ... | muscleN_L | muscleN_R |
|-----|---------|-----------|-----------|-----|-----------|-----------|
| P01 | d1      | 0         | 2         | ... | 2         | 1         |
| P02 | d1      | 1         | 0         | ... | 4         | 3         |
| P03 | d2      | 4         | 2         | ... | 3         | 0         |
| P04 | d2      | 4         | 0         | ... | 0         | 2         |

One column with name "id", with the identifier of the patient
One column with the name "disease", with the diagnosis of the patient
Columns for each muscle with the format <name>_<side>, where side can
be either "L" (left) or "R" (right).
"""
class MercuriTable:
    def __init__(
        self,
        df: pd.DataFrame = None,
        allowed_type: str = "int",
        allowed_range: tuple = (0, 4),
    ) -> None:
        self.df = df
        self.patients = []
        self.allowed_type = allowed_type
        self.allowed_range = allowed_range

        if isinstance(df, pd.DataFrame):
            self._check_invalid_headers()
            self._add_patients_from_df()

    def add_patient(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError("patient must be of type Patient")
        getattr(self, f"patients").append(patient)

    def from_csv(self, file, **kwargs):
        self.df = pd.read_csv(file, **kwargs)
        self._check_invalid_headers()
        self._add_patients_from_df()

    def from_excel(self, file, **kwargs):
        self.df = pd.read_excel(file, **kwargs)
        self._check_invalid_headers()
        self._add_patients_from_df()

    def _add_patients_from_df(self):
        if not isinstance(self.df, pd.DataFrame):
            print('Load a dataframe first.')
            return
        
        for idx, row in self.df.iterrows():
            p = Patient()
            p._load_from_row(row, self.allowed_type, self.allowed_range)
            self.add_patient(p)

    def _check_invalid_headers(self):
        for col in self.df.columns:
            if len(re.findall("[<>=\-()|&\d]", col)) > 0:
                raise Exception('Ilegal character found in column headers. Numbers are not allowed. The following characters are also not allowed: <>=-()|&')

    def disease_count(self):
        res = {}
        for p in self.patients:
            if not p.disease in res.keys():
                res[p.disease] = 0
            res[p.disease] += 1
        
        return pd.Series(res)
            

class Patient:
    def __init__(self, id=None, disease=None) -> None:
        self.id: str = id
        self.disease: str = disease
        self.muscles_L: dict = {}
        self.muscles_R: dict = {}

    def add_muscle(self, muscle, side: str) -> None:
        if not isinstance(muscle, Muscle):
            raise TypeError("muscle must be of type Muscle")
        if not isinstance(side, str):
            raise TypeError("side must be of type str")
        if not side in ["L", "R"]:
            raise ValueError('side must be "L" or "R"')
        getattr(self, f"muscles_{side}")[muscle.name] = muscle
        return None

    def _load_from_row(self, row, allowed_type, allowed_range):
        self.id = str(row.pop("id"))
        self.disease = str(row.pop("disease"))

        for m in list(row.index):
            m_split = m.split("_")
            m_name = "_".join(m_split[:-1])
            m_side = m_split[-1]
            getattr(self, f"muscles_{m_side}")[m_name] = Muscle(
                m_name, 
                m_side, 
                row[m], 
                allowed_type, 
                allowed_range
            )

class Muscle:
    def __init__(
        self,
        name: str,
        side: str,
        score,
        allowed_type: str = "int",
        allowed_range: tuple = (0, 4),
    ) -> None:
        if not allowed_type in ["int", "float"]:
            raise ValueError('allowed_type must be "int" or "float"')

        self.allowed_type = allowed_type
        self.allowed_range = allowed_range

        if self.allowed_type == "int":
            if pd.isna(score):
                self.score = np.nan
            else:
                if not float(score).is_integer():
                    warnings.warn(
                        f'allowed_type is "int", but the score has decimals. The score will be coerced to int and decimal values will be lost: Muscle {name}_{side}, Score {score}'
                    )
                self.score = int(float(score))
        elif self.allowed_type == "float":
            if pd.isna(score):
                self.score = np.nan
            else:
                self.score = float(score)
        else:
            raise ValueError('allowed_type must be "int" or "float"')

        if not self.allowed_range[0] <= self.score <= self.allowed_range[
            1
        ] and not np.isnan(self.score):
            raise ValueError(f"Mercuri score must be in range {allowed_range}")

        self.name = name
        self.side = side
