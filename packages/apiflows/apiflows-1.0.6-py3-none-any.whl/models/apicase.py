#!/bin/env pyton3

import json
import logging
import requests
import importlib
import xmltodict
from utils import parse_dict_with_extracts, extract_from_jsonpath
from colorama import init, Fore, Back, Style

class APICase(json.JSONEncoder):

    def __init__(self, config, name, url, method):
        """
        init
        """
        self.config = config
        self.name = name
        self.url = url
        self.method = method.upper()
        self.headers = config.HEADERS.copy()

    def set_name(self, name):
        """
        set name
        """
        self.name = name

    def set_url(self, url):
        """
        set url
        """
        self.url = url

    def set_method(self, method):
        """
        set method
        """
        self.method = method

    def set_headers(self, headers):
        """
        set headers
        """
        if headers:
            for _, key in enumerate(headers):
                self.headers[key] = str(headers[key])

    def set_header(self, key, value):
        """
        set header
        """
        self.headers[key] = str(value)

    def set_data(self, data):
        """
        set raw data
        """
        self.data = data if data else None

    def set_assertions(self, assertions):
        """
        set assertons
        """
        self.assertions = assertions if assertions else {}

    def set_extracts(self, extracts):
        """
        set extracts
        """
        self.extracts = extracts if extracts else {}

    def set_response(self, response):
        """
        set response
        """
        self.response = response

    def get_name(self):
        """
        get name/title
        """
        return self.name

    def get_url(self, is_parsed=False):
        """
        get url
        """
        if is_parsed:
            return parse_dict_with_extracts(self.config, self.url, '')
        return self.url

    def get_headers(self, is_parsed=False):
        """
        get headers
        """
        if is_parsed:
            return parse_dict_with_extracts(self.config, self.headers, '')
        return self.headers

    def get_data(self, is_parsed=False):
        """
        get raw data
        """
        if is_parsed:
            return parse_dict_with_extracts(self.config, self.data, '')
        return self.data

    def get_assertions(self, is_parsed=False):
        """
        get assertions
        """
        if is_parsed:
            return parse_dict_with_extracts(self.config, self.assertions, '')
        return self.assertions

    def get_extracts(self, is_parsed=False):
        """
        get extracts
        """
        if is_parsed:
            return parse_dict_with_extracts(self.config, self.extracts, '')
        return self.extracts

    def get_response(self):
        """
        get response
        """
        return self.response

    def do_request(self):
        """
        send request
        """
        headers = self.get_headers(True)
        url = self.get_url(True)
        data = self.get_data(True)

        response = None
        try:
            if (isinstance(data, dict)):
                response = requests.request(self.method, headers=headers, url=url, json=data)
            else:
                response = requests.request(self.method, headers=headers, url=url, data=data)
        except Exception as e:
            logging.error(Fore.RED + "    ERROR HTTP message:{}".format(e, ) + Fore.RESET)

        self.set_response(response)

    def parse_status_code(self):
        """
        parse response code
        """
        response = self.get_response()
        if response is None:
            return None

        return response.status_code
        
    def parse_response_headers(self):
        """
        parse response headers
        """
        response = self.get_response()
        if response is None:
            return None

        return dict(response.headers)

    def parse_response_body(self):
        """
        parse response
        """
        response = self.get_response()
        if response is None:
            return None
        
        resp_type = response.headers.get('Content-Type')
        if not resp_type:
            resp_type = str(self.get_headers().get('Content-Type'))
        
        try:
            if "xml" in resp_type:
                json_obj = xmltodict.parse(response.text)
            else:
                json_obj = json.loads(response.text)
            return json_obj
        except:
            # logging.error(Fore.RED + "    ERROR parsing response:" + resp.text + Fore.RESET)
            pass

        if response:
            return response.text

        return None

    def extractor(self, json_obj):
        """
        extract variables from response
        """
        exts = self.get_extracts()
        for _, var in enumerate(exts):
            v = exts[var]
            # extract from code/headers/body
            key = 'body'
            jp = v
            if isinstance(v, dict):
                key = v['in']
                jp = v['exp']
            self.config.EXTRACTS[var] = extract_from_jsonpath(jp, json_obj, key)
            logging.info("\t\tEXTRACT [{}]={}".format(var, self.config.EXTRACTS[var], ))

    def assertor(self, json_obj):
        """
        assertor
        """
        module_obj = None
        for _, assertion in enumerate(self.get_assertions()):
            comp = assertion['comparator']

            # load assertor
            module_name = "assertors." + comp
            func_name = "assert_" + comp
            module_obj = importlib.import_module(module_name)
            func = getattr(module_obj, func_name)
            # run real assertor
            func(self.config, self, assertion, json_obj)
        logging.info("")

    def __repr__(self) -> str:
        return json.dumps({
            "name": self.name,
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "data": self.data,
            "extracts": self.extracts,
            "assertions": self.assertions,
        })