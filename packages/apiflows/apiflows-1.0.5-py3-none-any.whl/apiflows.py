#!/bin/env python3

import os
import sys
import json
import glob
import yaml
from models.apicase import APICase
from colorama import init, Fore, Back, Style
import logging
import argparse
import importlib
from utils import parse_dict_with_extracts, extract_from_jsonpath

config = None

def initial():
    # Initializes Colorama
    init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--configfile',
        help="Config py file",
        type=str, dest="configfile",
        default="config.py"
    )
    parser.add_argument(
        '-t', '--testcases',
        help="Testcases yaml files directory",
        type=str, dest="testcases",
        default="./testcases"
    )
    parser.add_argument(
        '-o', '--output',
        help="Output file of test result location",
        type=str, dest="output",
        default="result.json"
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Show verbose info",
        action="count",
        default=1
    )
    args = parser.parse_args()
    loglevel = logging.WARNING - args.verbose * 10
    logging.basicConfig(level=loglevel, format='%(message)s')
    logging.getLogger("requests").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3").setLevel(logging.CRITICAL)

    config_path = os.path.dirname(os.path.abspath(args.configfile))
    if not os.path.isfile(args.configfile):
        logging.error(Fore.RED + "Config file not exists:" + args.configfile + Fore.RESET)
        sys.exit(1)
    
    logging.info("Starting test with config file: " + args.configfile + "\n")
    
    # loading config script
    if config_path:
        sys.path.append(config_path)

    # updating config
    global config
    module_name = os.path.basename(args.configfile).replace('.py', '')
    config = importlib.import_module(module_name)

    return args

def run_tests(apicases):
    # run tests
    for _, apicase in enumerate(apicases):
        name = apicase.get_name()
        logging.info("[" + name + "]: " + apicase.get_url())

        # pre request
        apicase = config.pre_request(apicase)

        # send HTTP request
        apicase = config.do_request(apicase)
        
        # post request
        config.post_request(apicase)
        if apicase.get_response() is None:
            continue

        json_obj = config.parse_response(apicase)
        logging.debug("\tJSON object:" + str(json_obj))

        # run extractor
        logging.info("\tEXTRACTOR: ")
        apicase.extractor(json_obj)
        # run assertor
        logging.info("\tASSERTIONS: ")
        apicase.assertor(json_obj)
    
    return apicases

def parse_apicases_from_yaml(config, file):
    """
    parse apicases from yaml
    """
    apicases = []
    with open(file, 'r') as f:
        data = yaml.safe_load(f.read())
        if not data.get('apicases'):
            return apicases
        
        for apiinfo in data.get('apicases'):
            parsed = parse_dict_with_extracts(config, apiinfo)

            # setup apicase
            apicase = APICase(config, parsed.get('name'), parsed.get('url'), parsed.get('method'))
            apicase.set_headers(parsed.get('headers'))
            apicase.set_data(parsed.get('data'))
            apicase.set_extracts(parsed.get('extracts'))
            apicase.set_assertions(parsed.get('assertions'))

            apicases.append(apicase)

    return apicases

def aft():
    args = initial()

    # pre testing
    config.pre_testing()

    # run tests
    pattern = (args.testcases + "/**/*.yaml") if os.path.isdir(args.testcases) else args.testcases
    files = sorted(glob.glob(pattern, recursive=True))

    results = []
    for i, filepath in enumerate(files):
        logging.info("{}:{}".format(i, filepath))
        apicases = parse_apicases_from_yaml(config, filepath)
        apicases = run_tests(apicases)
        results.append(apicases)
        logging.info("")
    
    with open(args.output, 'w') as f:
        # save test result to file
        logging.info("Saved test result to file:" + args.output)
        json.dump([json.loads(str(api)) for api in results], f, ensure_ascii=False, indent=4)

    # post testing
    config.post_testing()
    
if __name__ != 'main':
    aft()
