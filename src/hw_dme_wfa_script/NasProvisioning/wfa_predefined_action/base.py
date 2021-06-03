import json
import sys
from util.httpclient import CommonHttpClient
from util import common
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.constants import LUN_ID_CONVERT_URL
from hw_dme_ansible_core.constants import CHECK_TASK_URL


def init_client(param):
    token = param.get('x-user-token')
    if token in [None, '']:
        raise ScriptException('parsing token error')
    global CLIENT
    CLIENT = CommonHttpClient(common.getLocalIP(), 32018, True, False,
                              headers={'x-user-token': token})


def get(path, param=None):
    path = assembling_url(path, param)
    try:
        return CLIENT.get(path)
    except Exception as ex:
        print('Request exception, reason: %s' % ex)
        raise ScriptException('request exception')


def post(path, param=None):
    try:
        return CLIENT.post(path, param)
    except Exception as ex:
        print('Request exception, reason: %s' % ex)
        raise ScriptException('request exception')


def delete(path, param=None):
    path = assembling_url(path, param)
    try:
        return CLIENT.delete(path)
    except Exception as ex:
        print('Request exception, reason: %s' % ex)
        raise ScriptException('request exception')


def put(path, param=None):
    try:
        return CLIENT.put(path, param)
    except Exception as ex:
        print('Request exception, reason: %s' % ex)
        raise ScriptException('request exception')


def assembling_url(url, param):
    if param:
        datas = [str(key) + '=' + str(param[key]) for key in param]
        return url + '?' + '&'.join(datas)
    else:
        return url


def param_conversion(param):
    if type(param) != str:
        return param
    try:
        json_loads = json.loads(param.replace('\\', '')
                                .replace('\"\"', 'null'))
        copy_data = json_loads.copy()
        for key, value in json_loads.items():
            if value in [None, '', ['']]:
                copy_data.pop(key)
        print('Parsing Parameters success')
        return copy_data
    except json.decoder.JSONDecodeError:
        raise ScriptException('invalid parameter.')


def task_request(task_id):
    response = get(CHECK_TASK_URL % task_id)
    if response[0] == 200:
        return str(response[1], encoding='utf8')
    else:
        print('Check task request failed. rason: %s' % response)
        raise ScriptException('check task request failed.')


def check_empty_param(*name):
    args = sys.argv
    if len(args) < 2:
        raise ScriptException('param cannot be empty.')
    param = param_conversion(args[1])
    for i in name:
        if param.get(i) is None:
            raise ScriptException('param %s cannot be empty.' % i)
    return param


def get_param():
    args = sys.argv
    if len(args) < 2:
        return None
    else:
        return param_conversion(args[1])


def print_result(result):
    try:
        print(json.dumps(json.loads(result), indent=4))
    except json.decoder.JSONDecodeError:
        print(result)


def log(operation_name):
    def request_func(func):
        def do(*args):
            print('Start send request')
            response = func(*args)
            if response[0] == 200 or response[0] == 202:
                print('{0} request success, status: {1}'.format(operation_name, response[0]))
                return str(response[1], encoding='utf8')
            else:
                print('{0} request failed, status: {1}'.format(operation_name, response[0]))
                raise ScriptException(response)
        return do
    return request_func


def lun_id_convert_func(wwn):
    response = get(LUN_ID_CONVERT_URL % wwn)
    if response[0] == 200:
        return str(response[1], encoding='utf8')
    else:
        print('Get volumes by wwn failed, reason: %s.' % response)
        raise ScriptException('get volumes by wwn failed')
