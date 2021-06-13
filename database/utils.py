def norm_dict(data : dict) -> dict:
    out = {}
    for key,value in data.items():
        if type(value) == dict:
            value = norm_dict(value)
        elif value.__class__.__module__ != "builtins":
            value = str(value)
        out[key] = value
    return out