import json
import sys

import IP2Location

import settings
from logger import general_logger as log

from timeit import default_timer as timer


def db_exist(db_file):
    '''
    Check if BD file exists and return status code with error message in case of error
    '''
    try:
        open(db_file, 'r')
    except FileNotFoundError as e:
        log.exception(e)
        msg = "IP2Loc DB file not found."
        log.error(msg)
        return {'code': 500, 'msg': msg}
    return {'code': 200}


def ip2loc(db_file, addr):
    '''
    Return all found data for addr
    '''
    ip2loc = IP2Location.IP2Location()
    ip2loc.open(db_file)

    return ip2loc.get_all(addr)


def format_json(data):
    '''
    Format IP Location data to json
    {
        "city_name": "Bacoor",
        "country_code": "PH",
        "country_name": "Philippines",
        "region_name": "Cavite"
    }   
    '''
    data = {
        "city_name": data.city.decode("utf-8"),
        "country_code": data.country_short.decode("utf-8"),
        "country_name": data.country_long.decode("utf-8"),
        "region_name": data.region.decode("utf-8"),
    }
    return json.dumps(data)


def format_csv(data, delimiter):
    '''
    Format IP Location data to CSV with delimiter
    country_code;country_name;region_name;city_name
    PH;Philippines;Cavite;Bacoor
    '''
    csv_string = delimiter.join((
        data.country_short.decode("utf-8"),
        data.country_long.decode("utf-8"),
        data.region.decode("utf-8"),
        data.city.decode("utf-8"),
    ))

    return csv_string


def validate_qs(qs):
    '''
    Ensure that Query String has all required params. Throw an error if not
    '''
    required_params = ['ip', 'format']
    params_left = set(required_params) - set(qs.keys())
    if len(params_left) != 0:
        msg = [
            "Required params was not passed.",
            "Required: {}.".format(required_params),
            "Got: {}.".format(list(qs.keys())),
        ]
        msg = ' '.join(msg)
        log.error(msg)
        return {'code': 500, 'msg': msg}

    return {'code': 200}


def wrap_lambda(status, headers, body):
    '''
    Transform responce to API GW required format
    '''
    return {
        'statusCode': status,
        'headers': headers,
        'body': body
    }


def lambda_handler(event, context):
    '''
    Main AWS Lambda handler
    '''

    # Check if DB file exists
    v = db_exist(settings.DB_FILE)
    if v['code'] != 200:
        headers = {'Content-Type': 'application/json'}
        err = json.dumps({"ERROR": v['msg']})
        return wrap_lambda(500, headers, err)

    # Validate Query String
    qs = event["queryStringParameters"] if event["queryStringParameters"] else {}
    v = validate_qs(qs)
    if v['code'] != 200:
        headers = {'Content-Type': 'application/json'}
        err = json.dumps({"ERROR": v['msg']})
        return wrap_lambda(500, headers, err)

    addr = qs['ip']
    request_format = qs['format']

    # Get data from DB
    data = ip2loc(settings.DB_FILE, addr)

    if request_format == 'json':
        body = format_json(data)
        headers = {'Content-Type': 'application/json'}
        return wrap_lambda(200, headers, body)
    elif request_format == 'csv':
        headers = {'Content-Type': 'text/csv'}
        body = format_csv(data, settings.CSV_DELIMITER)
        return wrap_lambda(200, headers, body)


if __name__ == '__main__':
    event = {}
    event["queryStringParameters"] = {
        'ip': '1.10.248.17',
        'format': 'json',
    }

    start = timer()

    data = lambda_handler(event, 'bar')
    log.debug(data)

    end = timer()
    log.debug("Took {}s".format(end - start))
