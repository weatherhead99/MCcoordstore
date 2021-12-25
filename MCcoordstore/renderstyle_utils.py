# -*- coding: utf-8 -*-

from typing import Optional, Dict, Any, Union

def merge_dct_hierarch(d1: Dict, d2: Dict):
    for k,v in d2.items():
        if k not in d1:
            d1[k] = v
        elif isinstance(d1[k], dict):
            merge_dct_hierarch(d1[k], v)

def str_to_dct(k: str, v: Union[str, int], out: Optional[Dict[str,Any]] = None) -> Dict[str, Any]:
    items = k.strip().split(".")
    
    construct = {}
    construct_ref = construct
    for item in items[:-1]:
        if item not in construct_ref:
            construct_ref[item] = dict()
        construct_ref = construct_ref[item]
    
    construct_ref[items[-1]] = v
    if out is None:
        return construct
    
    merge_dct_hierarch(out, construct)
        
    return out

def strs_to_nested_dct(flatmap : Optional[Dict[str,Any]]):
    out = {}
    for k,v in flatmap.items():
        str_to_dct(k,v, out)
        print(k)
        print(out)
    return out
        

if __name__ == "__main__":
    
    form_input = {"marker.line.color" : "#ffffff",
                  "marker.color" : "#000000",
                  "marker.size" : 12,
                  "marker.line.width" : 4}
    
    d = strs_to_nested_dct(form_input)
    