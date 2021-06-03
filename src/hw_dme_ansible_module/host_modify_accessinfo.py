#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.host import update_accessinfo

DOCUMENTATION = r'''
---
module: host_modify_accessinfo
description:
  - Modify a host.
Options:
  dme_ip:
    description:
      - DME IP.
    type: str
    required: true
  dme_port:
    description:
      - Northbond api port, default: 26335
    type: str
    required: false
  dme_user:
    description:
      - Northbond api username.
    type: str
    required: true
  dme_password:
    description:
      - Northbond api password.
    type: str
    required: true
  dme_certificate_path:
    description:
      - DME certificate path.
    type: str
    required: false
  host_id:
    description:
      - Host ID.
      - Parameter length: 1 to 64.
    type: str
    required: true
  ip:
    description:
      - IP address for adding a host.
      - Parameter length: 0 to 127.
    type: str
    required: false
  port:
    description:
      - Port for adding the host.
    type: str
    required: false
  username:
    description:
      - Username for adding a host.
      - Parameter length: 1 to 255.
    type: str
    required: false
  password:
    description:
      - Password for adding a host.
      - Parameter length: 1 to 1024.
    type: str
    required: false
  project_id:
    description:
      - Project ID.
      - Parameter length: 0 to 64.
    type: str
    required: false
  azs:
    description:
      - AZ ID list.
      - Parameter length: 1 to 64.
    type: str
    required: false
  sync_to_storage:
    description:
      - Auto modifying the host name, IP address, and OS in the storage system during host modification.
      - If this parameter is left blank, the default value is false.
    type: str
    required: false
  description:
    description:
      - Host description modification.
      - Parameter length: 0 to 63.
    type: str
    required: false
  multipath_type:
    description:
      - Multipathing software type.
      - Value range:
        - default
        - third_party
    type: str
    required: false
  path_type:
    description:
      - Path type of an initiator.
      - Value range:
        - optimal_path
        - non_optimal_path
    type: str
    required: false
  failover_mode:
    description:
      - Switchover mode of an initiator.
      - Value range:
        - early_version_alua (early-version ALUA)
        - common_alua (hw_dme_ansible_core ALUA)
        - alua_not_used (ALUA not used)
        - special_alua (special mode)
    type: str
    required: false
  special_mode_type:
    description:
      - Special mode type of an initiator.
      - Value range:
        - mode_zero
        - mode_one
        - mode_two
        - mode_three
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def host_update_request_func(host_id, param):
        return ansible_base.put(constants.HOST_MODIFY_ACCESSINFO_URL % host_id,
                                param)

    result = {}
    try:
        result['data'] = update_accessinfo(params, host_update_request_func)
        result['msg'] = 'Host is successfully updated.'
    except ScriptException as ex:
        result['msg'] = 'Host fails to be updated. Fault cause: %s.' % ex
        result['failed'] = True

    module.exit_json(**result)


def main():
    argument_spec = dict(
        host_id=dict(required=True, type='str'),
        ip=dict(required=False, type='str'),
        port=dict(required=False, type='str'),
        username=dict(required=False, type='str'),
        password=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
        azs=dict(required=False, type='str'),
        sync_to_storage=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        multipath_type=dict(required=False, type='str'),
        path_type=dict(required=False, type='str'),
        failover_mode=dict(required=False, type='str'),
        special_mode_type=dict(required=False, type='str'),
    )
    argument_spec.update(ARGUMENT_SPEC_BASE)
    module = AnsibleModule(
        argument_spec=argument_spec
    )
    params = module.params
    ansible_base = AnsibleBase(params['dme_ip'],
                               params['dme_port'],
                               params['dme_user'],
                               params['dme_password'],
                               params['dme_certificate_path'])
    run_module(params, ansible_base, module)


if __name__ == '__main__':
    main()
