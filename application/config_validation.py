from application import config

def indentIsValid():
    try:
        indent=int(config.get('settings','outputIndent'))
    except ValueError:
        indent=4
        return False
    else:
        return True

def formatIsValid():
    if str(config.get('settings','outputIndent')).lower() not in ['json', 'yaml']:
        return 'Output format is not valid. Value must be one of \'json\' or \'yaml\''
    else:
        return True
        