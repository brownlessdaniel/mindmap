from application import config, process_output

@process_output.formatOutput
def updateConfig(args):
    '''
    Takes a dictionary of arguments, from which it extracts the setting and value.
    Checks that the specified setting and value are valid, then writes the
    changes to the config.ini file.
    Returns confirmation of config change.
    Returns dictionary.
    '''
    setting = args.get('setting')
    value = args.get('value')
    valid_outputformats=["json","yaml"]

    if setting not in (config.options('settings')):
        return {'status': 'error','msg':f'Invalid setting - valid settings are {config.options("settings")}'}
    if setting == 'outputformat' and value.lower() not in valid_outputformats:
        return {'status': 'error','msg':"Invalid value for 'outputformat' - valid settings are 'json' or 'yaml'"}
    if setting == 'databasepath':
        return {'status': 'error','msg':"I can't do that yet!'"}
    if setting == 'outputindent' and not value.isnumeric():
        return {'status': 'error','msg':"Invalid value for 'outputindent' - value must be a number!'"}
    if setting == 'outputindent' and int(value)>10:
        return {'status': 'error','msg':"Invalid value for 'outputindent' - value must be less than 10!'"}
    
    setting=str(setting)
    value=str(value)
    
    with open('application/config.ini', 'w') as configfile:
        config.set('settings', setting, value)
        config.write(configfile)
    output = {'status': 'success','msg':f'{setting} set to {value}!'}
    return output
