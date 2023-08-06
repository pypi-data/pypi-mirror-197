#!/bin/env python3

import uuid
import logging

# common headers
HEADERS = {
    'content-type': 'application/json',
    'x-token': '1234',
}

# common extracts
EXTRACTS = {
    'USERNAME':'allen'
}

def pre_testing():
    """
    pre testing
    """
    logging.debug("pre_testing()...")
    HEADERS['x-apiflows-id'] = str(uuid.uuid4())

def pre_request(apicase):
    """
    pre request
    """
    # TODO here
    logging.debug("pre_request()...")
    apicase.set_header("mycookie", "PHPSESSIONID=apiflows")
    return apicase

def do_request(apicase):
    logging.debug("do_request()...")
    apicase.do_request()
    return apicase

def parse_response(apicase):
    """
    parse HTTP response
    """
    logging.debug("parse_response()...")
    code = apicase.parse_status_code()
    headers = apicase.parse_response_headers()
    body = apicase.parse_response_body()
    return {'code': code, 'headers': headers, 'body': body}

def post_request(apicase):
    """
    post request
    """
    # TODO
    logging.debug("post_request()...")
    response = apicase.get_response()
    if response is not None:
        logging.debug("    RESPONSE: " + response.text)
    
    return apicase

def post_testing():
    """
    post testing
    """
    # TODO
    logging.debug("post_testing()...")