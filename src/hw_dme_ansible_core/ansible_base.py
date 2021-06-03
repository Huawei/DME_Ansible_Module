# -*- coding: utf-8 -*
import requests
import os
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.common import del_none_key
from urllib.parse import urljoin

ARGUMENT_SPEC_BASE = dict(
        dme_ip=dict(required=True, type='str'),
        dme_port=dict(required=False, type='str', default='26335'),
        dme_user=dict(required=True, type='str'),
        dme_password=dict(required=True, type='str'),
        dme_certificate_path=dict(required=False, type='str'))


def request_wrapper(func):
    def do(*args):
        if args[0].headers is None:
            args[0].login()
        try:
            response = func(*args)
        except Exception as ex:
            raise ScriptException(ex)
        if response.status_code in [200, 202]:
            return response.text
        else:
            raise ScriptException('status code {0}, response is {1}'.format(response.status_code, response.text))
    return do


def get_certificate_path(verify):
    if not verify:
        return False
    if os.path.isfile(verify):
        return verify
    return False


class AnsibleBase:

    def __init__(self, ip, port, user, password, verify=False):
        self.prefix_url = 'https://{0}:{1}'.format(ip, port)
        self.verify = get_certificate_path(verify)
        self.user = user
        self.password = password
        self.headers = None

    def login(self):
        try:
            body = {"grantType": "password", "userName": self.user,
                    "value": self.password}
            response = requests.put(
                urljoin(self.prefix_url, constants.LOGIN_URL), json=body,
                verify=self.verify)
        except Exception as e:
            raise ScriptException(
                'northbound authentication failed. Fault cause: %s' % e)
        if response.status_code != 200:
            raise ScriptException(
                'northbound authentication failed. states code: %s' % response.status_code)
        session = response.json()['accessSession']
        self.headers = {'X-Auth-Token': session}

    @request_wrapper
    def task_request(self, task_id):
        task_path = urljoin(self.prefix_url, constants.CHECK_TASK_URL % task_id)
        return requests.get(task_path, headers=self.headers, verify=self.verify)

    @request_wrapper
    def get(self, url, param=None):
        param = del_none_key(param)
        path = urljoin(self.prefix_url, url)
        return requests.get(path, param, headers=self.headers,
                            verify=self.verify)

    @request_wrapper
    def post(self, url, body):
        body = del_none_key(body)
        path = urljoin(self.prefix_url, url)
        return requests.post(path, json=body, headers=self.headers,
                             verify=self.verify)

    @request_wrapper
    def put(self, url, body):
        body = del_none_key(body)
        path = urljoin(self.prefix_url, url)
        return requests.put(path, json=body, headers=self.headers,
                            verify=self.verify)

    @request_wrapper
    def delete(self, url, param):
        param = del_none_key(param)
        path = urljoin(self.prefix_url, url)
        return requests.delete(path, params=param, headers=self.headers,
                               verify=self.verify)

    def lun_id_convert_func(self, wwn):
        try:
            return self.get(constants.LUN_ID_CONVERT_URL % wwn)
        except ScriptException as ex:
            raise ScriptException('get volumes by wwn failed, %s' % ex)
