# -*- coding: utf-8 -*
import json
import time


STATUS_MAP = {1: 'Not Start', 2: 'Running', 3: 'Succeeded',
              4: 'Partially Succeeded', 5: 'Failed',
              6: 'Timeout', 7: 'Warning'}


def check_task(check_task_request, task_id):
    retry_times = 120
    task_status = None
    now_task = None
    while retry_times > 0:
        task_values = json.loads(check_task_request(task_id))
        for task in task_values:
            if task['id'] == task_id:
                now_task = task
        task_status = now_task['status']

        if task_status not in [None, 1, 2]:
            break

        time.sleep(1)
        retry_times = retry_times - 1
    if retry_times == 0:
        raise ScriptException('checking the task status timed out.')
    if task_status == 3:
        return STATUS_MAP.get(task_status)
    elif task_status == 7:
        return STATUS_MAP.get(task_status) + \
               '\n' + now_task.get('detail_en')
    else:
        raise ScriptException(STATUS_MAP.get(task_status) +
                              '\n' + now_task.get('detail_en'))


def list_param_conversion(param=None, *key):
    for i in key:
        if param.get(i):
            param[i] = param.get(i).split(',')


def check_empty_param(params, *name):
    if params is None:
        raise ScriptException('param cannot be empty.')
    for i in name:
        if params.get(i) is None:
            raise ScriptException('param %s cannot be empty.' % i)


# wwn 转换为volumes_id
def volume_id_conversion(wwn, lun_id_convert_func):
    if wwn is None:
        raise ScriptException('Volume wwn cannot be empty.')
    response = lun_id_convert_func(wwn)
    try:
        return json.loads(response)['volumes'][0]['id']
    except Exception as ex:
        print('Parsing volume id failed, reason: %s' % ex)
        raise ScriptException('parsing volume id failed')


# wwns 转换为volumes_ids
def volume_ids_conversion(wwns, lun_id_convert_func):
    if wwns is None:
        raise ScriptException('volume wwns cannot be empty.')
    wwn_list = wwns.split(',')
    volume_ids = [volume_id_conversion(i, lun_id_convert_func) for i in wwn_list]

    return volume_ids


def del_none_key(body):
    if not body:
        return body
    copy_data = body.copy()
    for key, value in body.items():
        if value in [None, '']:
            copy_data.pop(key)
    return copy_data


class ScriptException(Exception):
    def __init__(self, msg):
        self.msg = msg


def build_body(keys, param):
    return {key: value for key, value in param.items() if key in keys}
