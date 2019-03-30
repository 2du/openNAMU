from .tool.func import *

def api_version_2(conn, r_ver, c_ver):
    curs = conn.cursor()

    new_ver = ''
    data = None

    try:
        if flask.request.host != 'namu.ml':
            data = urllib.request.urlopen('https://namu.ml/api/version')
    except:
        pass

    if data and data.getcode() == 200:
        try:
            json_data = json.loads(data.read().decode(data.headers.get_content_charset()))
            if 'version' in json_data:
                new_ver = json_data['version']
        except:
            pass
        
    json_data = { "version" : r_ver, "db_version" : c_ver, "lastest_version" : new_ver  }

    return flask.jsonify(json_data)