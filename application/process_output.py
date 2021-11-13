import json
import yaml
from pathlib import Path
import os
from collections import OrderedDict
from sqlalchemy import inspect
from application import base, session, Node, config

# from application.database_operations import describe

def formatOutput(func):
    '''
    Decorator function that formats output as specified in confing.ini.
    
    TODO: Config file validation must happen somewhere else.

    TODO: since dicts are not ordered, pyaml dumps thins without order. Look into OrderedDict
    '''    
    output_format = config.get('settings','outputFormat').lower()
    output_indent = int(config.get('settings', 'outputIndent'))

    if output_format == 'json':
        def wrapper(*args, **kwargs):
            print(json.dumps(func(*args, **kwargs),indent=output_indent))
            return ''
        
        return wrapper

    # elif output_format == 'yaml':
    #     def wrapper(*args, **kwargs):
    #         yaml.dump(func(*args, **kwargs),default_flow_style=False,indent=output_indent)
    #     return wrapper

def outputSettings(func):
    '''
    Decorator function that implaments, verbose, debug and descriptive settings.

    verbose --> Json output e.g. 'message: success' Default: On
    descriptive --> Calls describe() each time database operation is performed.
    debug --> prints info such as Namespace, aux arguments etc.
    '''
    verbose = config.get('settings', 'verbose').lower()
    debug = config.get('settings', 'debug').lower()
    descriptive = config.get('settings', 'descriptive').lower()

    def wrapper(*args, **kwargs):
        # func(*args, **kwargs)
        if descriptive == 'true' and func.__name__ != 'describe':
                output = func(*args, **kwargs), describe()
        else:
            output = func(*args, **kwargs)
        return output
    return wrapper
    

# This function needs to be accessible by outputSettings and database operations..
def describe(filter=None):
    '''
    Outputs entire contents of database.
    Allows filtering.
    '''
    output = OrderedDict()

    for n in session.query(Node).all():
        output[n.id] = {c.key: getattr(n, c.key) for c in inspect(n).mapper.column_attrs}

    return output