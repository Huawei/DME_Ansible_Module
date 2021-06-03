import json
import re
import sys

from util import common
from util.httpclient import CommonHttpClient


class ScriptException(Exception):
    def __init__(self):
        pass


def check(response):
    if response[0] != 200:
        raise ScriptException()
    return json.loads(response[1])


class ParamIR:

    def __init__(self, token):
        self.client = CommonHttpClient(common.getLocalIP(), 32018, True, False,
                                       headers={'x-user-token': token})

    def get(self, path, param=None):
        path = build_url(path, param)
        return check(self.client.get(path))

    def post(self, path, param=None):
        return check(self.client.post(path, param))

    def delete(self, path, param=None):
        path = build_url(path, param)
        return check(self.client.delete(path))

    def put(self, path, param=None):
        return check(self.client.put(path, param))


def get_param(*name):
    args = sys.argv
    if len(args) < 2:
        raise ScriptException()
    else:
        param = json.loads(args[1])
        token = param.get('x-user-token')
        if token is None:
            raise ScriptException()
        param.pop('x-user-token')
        for i in name:
            if param.get(i) is None:
                raise ScriptException()
        return token, param


def build_url(url, param):
    if param:
        datas = ['{}={}'.format(str(key), str(param[key])) for key in param]
        return url + '?' + '&'.join(datas)
    else:
        return url


def get_storage_pool_result(info):
    # Tier0 对应的硬盘类型，，0-无效，3-SSD，10-SSD_SED，14-NVMe SSD，16-NVMe SSD SED
    # Tier1 对应的硬盘类型，，0-无效，1-SAS，8-SAS SED
    # Tier2 对应的硬盘类型，，0-无效，2-SATA，4-NL-SAS，11-NL-SAS SED。
    tier0 = {'0': '--', '3': 'SSD', '10': 'SSD SED', '14': 'NVMe SSD',
             '16': 'NVMe SSD SED'}
    tier1 = {'0': '--', '1': 'SAS', '8': 'SAS SED'}
    tier2 = {'0': '--', '2': 'SATA', '4': 'NL-SAS', '11': 'NL-SAS SED'}
    fs_subscribed_capacity = info.get('fs_subscribed_capacity')
    total_capacity = info.get('total_capacity')
    tier0_disk_type = info.get('tier0_disk_type')
    tier1_disk_type = info.get('tier1_disk_type')
    tier2_disk_type = info.get('tier2_disk_type')
    disk_type = ''
    if tier0_disk_type and tier0_disk_type != '0':
        disk_type += tier0.get(tier0_disk_type) + '/'
    if tier1_disk_type and tier1_disk_type != '0':
        disk_type += tier1.get(tier1_disk_type) + '/'
    if tier2_disk_type and tier2_disk_type != '0':
        disk_type += tier2.get(tier2_disk_type) + '/'
    if disk_type != '--':
        disk_type = disk_type[:-1] + ''
    used_capacity_radio = format(fs_subscribed_capacity / total_capacity, '.0%')
    remaining_capacity = int((total_capacity - fs_subscribed_capacity) / 1024)
    value = '{}（剩余容量：{}，已分配：{}，{}）'.format(info.get('name'),
                                           str(get_capacity(remaining_capacity)),
                                           str(used_capacity_radio),
                                           str(disk_type))
    return value


def get_storage_result(info):
    name = info.get('name')
    usableCapacity = info.get('usableCapacity')
    subscription_capacity = info.get('subscription_capacity')
    used_capacity_radio = format(subscription_capacity / usableCapacity, '.0%')
    remaining_capacity = int(
        (usableCapacity - subscription_capacity) / (1024))

    # used_capacity已用容量（单位: MB）。
    # total_capacity总容量（单位: MB）。
    # subscription_capacity订阅容量：（所有pool的文件系统分配容量之和 + 所有pool的LUN分配容量之和）。
    return '{}（剩余容量：{}，已分配：{}）'.format(name, str(get_capacity(remaining_capacity)),
                                       str(used_capacity_radio))


def get_ip_b(ips_params):
    ips_params_new = []
    for ip in ips_params:
        if ip:
            nums = ip.split('.')
            if len(nums) >= 2:
                ip = '{}.{}'.format(str(nums[0]), str(nums[1]))
                ips_params_new.append(ip)
    return ips_params_new


def is_dorado_device(storage_info):
    # 判断dorado v6设备
    model_lower_case = str(storage_info.get('model')).lower()
    storage_product_version = storage_info.get('version')
    dorado = re.search(r'dorado', model_lower_case)
    nas = re.search(r'v6', model_lower_case)
    if dorado and nas and storage_product_version >= '6.1.0':
        return True
    return False


def get_capacity(capacity):
    sign = ''
    if capacity < 0:
        sign = '-'
    capacity = abs(capacity)
    if capacity >= 1024:
        value = float(format(float(capacity) / 1024, '.2f'))
        if value >= 1024:
            return sign + format(float(value) / 1024, '.2f') + 'PB'
        return sign + str(value) + 'TB'
    else:
        return sign + str(capacity) + 'GB'


def get_storage_info(client, storage_id):
    storage_infos = client.get(
        "/rest/storagemgmt/v1/storages?start=1&limit=100").get("datas")
    for info in storage_infos:
        if storage_id == info['id']:
            return info
