import json
import yaml
from collections import OrderedDict
from application import base, session, Node
from application import config
# from application.database_operations import describe

def describe(filter=None):
    '''
    Outputs entire contents of database.
    Allows filtering.
    '''
    output = {}
    for n in session.query(Node).all():
        attributes = {}
        
        attributes['master']=n.master
        attributes['parent']=n.parent
        attributes['label']=n.label
        attributes['note']=n.note
        attributes['doc']=n.doc
        attributes['colour']=n.colour
        attributes['hidden']=n.hidden
        attributes['hide_children']=n.hide_children
        output[n.uid]=attributes
    return output




def formatOutput(func):
    '''
    Decorator function that formats output as specified in confing.ini.
    
    TODO: Config file validation must happen somewhere else.

    TODO: since dicts are not ordered, pyaml dumps thins without order. Look into OrderedDict
    '''    
    output_format = config.get('settings','outputFormat').lower()
    output_indent = int(config.get('settings', 'outputIndent'))
    descriptive = bool(config.get('settings', 'descriptive').lower())

    if output_format == 'json':
        def wrapper(*args, **kwargs):
            print(json.dumps(func(*args, **kwargs),indent=output_indent))
            if descriptive:
                print(describe())
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
        if descriptive:
            describe()
        # print('test')
    return wrapper
    