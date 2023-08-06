#!/bin/env python3

import logging
from utils import extract_from_jsonpath, parse_dict_with_extracts
from colorama import init, Fore, Back, Style
import re

def assert_match(config, apicase, assertion, json_obj):
    key = assertion.get('in', 'body')
    exp1 = extract_from_jsonpath(parse_dict_with_extracts(config, assertion['exp1']), json_obj, key)
    exp2 = parse_dict_with_extracts(config, assertion['exp2'])

    if exp1 and re.search(exp2, exp1) != None:
        message = "{} = {} [match] {}".format(assertion['exp1'], exp1, exp2, )
        assertion['message'] = message
        assertion['result'] = True
        logging.info("\t\t" + Fore.GREEN + message + Fore.RESET)
        return True
    
    message = "{} = {} [match] {}".format(assertion['exp1'], exp1, exp2, )
    assertion['message'] = message
    assertion['result'] = False
    logging.warning("\t\t" + Fore.RED + message + Fore.RESET)
    return False