def increment(d:dict, k:str) -> dict:
    if k in d.keys(): d[k] += 1 
    else: d[k] = 1
    return d