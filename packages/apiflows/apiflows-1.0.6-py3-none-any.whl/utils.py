#!/bin/env python3

import logging
from jsonpath_ng import parse as parse_jsonpath
from colorama import init, Fore, Back, Style

def parse_dict_with_extracts(config, obj, key=None):
    """
    parse api with extracts
    """
    if isinstance(obj, (int, float)):
        obj = obj
        return obj
    
    if isinstance(obj, str):
        old = obj
        for K in config.EXTRACTS:
            V = config.EXTRACTS[K]
            place_holder = '{{' + K + '}}'
            if place_holder in obj:
                if V is not None:
                    obj = obj.replace(place_holder, V)
                    logging.debug(Fore.GREEN + "\t\tParsed {}:{} to {}".format(key, old, obj, ) + Fore.RESET)
                else:
                    logging.warn(Fore.RED + "\t\tParsed FAIL {}:{}".format(key, old, ) + Fore.RESET)
        return obj

    if not isinstance(obj, dict):
        return obj
    
    for k in obj:
        obj[k] = parse_dict_with_extracts(config, obj[k], k)
    return obj

def extract_from_jsonpath(jp, json_obj, key):
    """
    extract variables from response by jsonpath
    """
    if jp:
        if '$' in str(jp):
            try:
                if key:
                    matches = parse_jsonpath(jp).find(json_obj[key])
                else:
                    matches = parse_jsonpath(jp).find(json_obj)
                
                if len(matches) > 0:
                    return str(matches[0].value)
                return None
            except:
                # logging.error('ERROR ' + jp + ' jsonpath not found in ' + str(json_obj))
                return None
        else:
            return str(jp)
    return str(jp)