# This is a Python implementation of the following jsonLogic JS library:
# https://github.com/jwadhams/json-logic-js
from __future__ import unicode_literals
#from automation_trigger import send_startTime

import sys
from tracemalloc import start
from more_itertools import difference, first
from six.moves import reduce
import logging

import array as arr
from tinydb import TinyDB, Query, where

from datetime import datetime
from dateutil import parser


db_camera = TinyDB('../database/camera_data.json')
db_general = TinyDB('../database/general_info.json')

query = Query()

logger = logging.getLogger(__name__)

try:
    unicode
except NameError:
    pass
else:
    # Python 2 fallback.
    str = unicode

def set_vehicleType_name(vehicleType):
    if vehicleType == 'CAR':
        return 'Car'
    elif vehicleType == 'TRUCK':
        return 'Truck'
    elif vehicleType == 'BICYCLE':
        return 'Bicycle'

def if_(*args):
    """Implements the 'if' operator with support for multiple elseif-s."""
    for i in range(0, len(args) - 1, 2):
        if args[i]:
            return args[i + 1]
    if len(args) % 2:
        return args[-1]
    else:
        return None


def soft_equals(a, b):
    """Implements the '==' operator, which does type JS-style coertion."""
    if isinstance(a, str) or isinstance(b, str):
        return str(a) == str(b)
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) is bool(b)
    return a == b


def hard_equals(a, b):
    """Implements the '===' operator."""
    if type(a) != type(b):
        return False
    return a == b


def less(a, b, *args):
    """Implements the '<' operator with JS-style type coertion."""
    types = set([type(a), type(b)])
    if float in types or int in types:
        try:
            a, b = float(a), float(b)
        except TypeError:
            # NaN
            return False
    return a < b and (not args or less(b, *args))


def less_or_equal(a, b, *args):
    """Implements the '<=' operator with JS-style type coertion."""
    return (
        less(a, b) or soft_equals(a, b)
    ) and (not args or less_or_equal(b, *args))


def to_numeric(arg):
    """
    Converts a string either to int or to float.
    This is important, because e.g. {"!==": [{"+": "0"}, 0.0]}
    """
    if isinstance(arg, str):
        if '.' in arg:
            return float(arg)
        else:
            return int(arg)
    return arg


def plus(*args):
    """Sum converts either to ints or to floats."""
    return sum(to_numeric(arg) for arg in args)


def minus(*args):
    """Also, converts either to ints or to floats."""
    if len(args) == 1:
        return -to_numeric(args[0])
    return to_numeric(args[0]) - to_numeric(args[1])


def merge(*args):
    """Implements the 'merge' operator for merging lists."""
    ret = []
    for arg in args:
        if isinstance(arg, list) or isinstance(arg, tuple):
            ret += list(arg)
        else:
            ret.append(arg)
    return ret


def get_var(data, var_name, not_found=None):
    """Gets variable value from data dictionary."""
    try:
        for key in str(var_name).split('.'):
            try:
                data = data[key]
            except TypeError:
                data = data[int(key)]
    except (KeyError, TypeError, ValueError):
        return not_found
    else:
        return data


def missing(data, *args):
    """Implements the missing operator for finding missing variables."""
    not_found = object()
    if args and isinstance(args[0], list):
        args = args[0]
    ret = []
    for arg in args:
        if get_var(data, arg, not_found) is not_found:
            ret.append(arg)
    return ret


def missing_some(data, min_required, args):
    """Implements the missing_some operator for finding missing variables."""
    if min_required < 1:
        return []
    found = 0
    not_found = object()
    ret = []
    for arg in args:
        if get_var(data, arg, not_found) is not_found:
            ret.append(arg)
        else:
            found += 1
            if found >= min_required:
                return []
    return ret


def function_vehicle_detection(zone, vehicleType):
    vehicle = set_vehicleType_name(vehicleType)
    #start_time = '2022-05-16T19:45:35.461Z'
    time = [query.get('start_time') for query in db_general.all()]
    start_time = time[0]

    if vehicleType == 'ALL':
        docs = db_camera.search((query.Task == 'Counter') & (
            query.Zone == zone) & (query.UtcTime > start_time))
    else:
        docs = db_camera.search((query.Task == 'Counter') & (
            query.Vehicle == vehicle) & (query.Zone == zone) & (query.UtcTime > start_time))

    i = 0
    for doc in docs:
        i += 1
        if i == 1:
            first_count = doc.get('Count')
        count = doc.get('Count')
   
    first_count = int(first_count)
    count = int(count)

    return abs(count-first_count)


def function_flow(zone, vehicleType, duration):    
    vehicle = set_vehicleType_name(vehicleType)
    #start_time = '2022-05-26T15:24:30.577383Z'
    time = [query.get('start_time') for query in db_general.all()]
    start_time = time[0]

    count_flow = -1
    first_count = -1

    if vehicleType == 'ALL':
        docs = db_camera.search((query.Task == 'Counter') & (
            query.Zone == zone) & (query.UtcTime > start_time))
    else:
        docs = db_camera.search((query.Task == 'Counter') & (query.Zone == zone) & (
            query.Vehicle == vehicle) & (query.UtcTime > start_time))

    i = 0
    j = 0 
    timeout = 0
    start_time = parser.parse(start_time)
    first_duration = -1

    for doc in docs:
        doc_time = parser.parse(doc.get('UtcTime'))
        amount = doc_time - start_time
        
        i += 1
        if i == 1:
            first_count = doc.get('Count')
        if(amount.total_seconds() > int(duration)):
            j += 1
            if j == 1:
                count_flow = doc.get('Count')
                first_duration = amount.total_seconds()
                timeout = 1
    
    first_count = int(first_count)
    count_flow = int(count_flow)

    detected_vehicles = abs(count_flow - first_count)

    print("       [DURATION]: " + str(duration) + "s  | [Amount]: " + str(first_duration) + "s  | [Already Counted]: " + str(first_count) + " | [Counted]: " + str(count_flow))    

    if timeout == 1:
        print("       [FLOW]: " + str(detected_vehicles) + " vehicles detected in " + str(duration) + " seconds" )
        return count_flow - first_count 
    else:
        print("No timeout")
        return 0 


def function_stay_time(zone, vehicleType):
    vehicle = set_vehicleType_name(vehicleType)
    #start_time = '2022-05-16T19:45:35.461Z'
    time = [query.get('start_time') for query in db_general.all()]
    start_time = time[0]

    if vehicleType == 'ALL':
        docs = db_camera.search(
            (query.Task == 'IdleObject') & (query.UtcTime > start_time))
    else:
        docs = db_camera.search((query.Task == 'IdleObject') & (
            query.Vehicle == vehicle) & (query.UtcTime > start_time))

    stayTime = 0
    #IMCOMPLETO
    return stayTime


def function_jam_detection(zone):
    #start_time = '2022-05-16T19:45:35.461Z'

    time = [query.get('start_time') for query in db_general.all()]
    start_time = time[0]
    
    docs = db_camera.search((query.Task == 'Jam Detection') & (query.UtcTime > start_time) & (query.Zone == zone))

    jam = False
    if docs:
        jam = True
        print("There is a JAM")

    return jam


def function_crowd_detection(zone):
    #start_time = '2022-05-16T19:45:35.461Z'

    time = [query.get('start_time') for query in db_general.all()]
    start_time = time[0]
    
    docs = db_camera.search((query.Task == 'Crowd Detection') & (query.UtcTime > start_time) & (query.Cam == zone))

    crowd = False
    if docs:
        crowd = True

    return crowd


operations = {
    "==": soft_equals,
    "===": hard_equals,
    "!=": lambda a, b: not soft_equals(a, b),
    "!==": lambda a, b: not hard_equals(a, b),
    ">": lambda a, b: less(b, a),
    ">=": lambda a, b: less(b, a) or soft_equals(a, b),
    "<": less,
    "<=": less_or_equal,
    "!": lambda a: not a,
    "!!": bool,
    "%": lambda a, b: a % b,
    "and": lambda *args: reduce(lambda total, arg: total and arg, args, True),
    "or": lambda *args: reduce(lambda total, arg: total or arg, args, False),
    "?:": lambda a, b, c: b if a else c,
    "if": if_,
    "log": lambda a: logger.info(a) or a,
    "in": lambda a, b: a in b if "__contains__" in dir(b) else False,
    "cat": lambda *args: "".join(str(arg) for arg in args),
    "+": plus,
    "*": lambda *args: reduce(lambda total, arg: total * float(arg), args, 1),
    "-": minus,
    "/": lambda a, b=None: a if b is None else float(a) / float(b),
    "min": lambda *args: min(args),
    "max": lambda *args: max(args),
    "merge": merge,
    "count": lambda *args: sum(1 if a else 0 for a in args),
    "vehicleDetection": function_vehicle_detection,
    "flow": function_flow,
    "stayTime": function_stay_time,
    "jamDetection": function_jam_detection,
    "crowdDetection": function_crowd_detection
}


def jsonLogic(tests, data=None):
    """Executes the json-logic with given data."""
    # You've recursed to a primitive, stop!
    if tests is None or not isinstance(tests, dict):
        return tests

    data = data or {}

    operator = list(tests.keys())[0]
    values = tests[operator]

    # Easy syntax for unary operators, like {"var": "x"} instead of strict
    # {"var": ["x"]}
    if not isinstance(values, list) and not isinstance(values, tuple):
        values = [values]

    # Recursion!
    values = [jsonLogic(val, data) for val in values]

    if operator == 'var':
        return get_var(data, *values)
    if operator == 'missing':
        return missing(data, *values)
    if operator == 'missing_some':
        return missing_some(data, *values)

    if operator not in operations:
        raise ValueError("Unrecognized operation %s" % operator)

    return operations[operator](*values)
