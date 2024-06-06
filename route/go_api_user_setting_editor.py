from .tool.func import *

def api_user_setting_editor():
    other_set = {}
    other_set["ip"] = ip_check()
    
    func_name = sys._getframe().f_code.co_name
    if flask.request.method == 'POST':
        func_name += '_insert'
        other_set['data'] = flask.request.form.get('data', 'Test')
    elif flask.request.method == 'DELETE':
        func_name += '_delete'
        other_set['data'] = flask.request.form.get('data', 'Test')

    return flask.Response(response = python_to_golang(func_name, other_set), status = 200, mimetype = 'application/json')