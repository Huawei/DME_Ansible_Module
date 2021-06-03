# -*- coding: utf-8
from hw_dme_ansible_core.hostgroup import delete
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: hostgroup_delete
description:
  - Delete a specified host group.
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
  hostgroup_id:
    description:
      - Host group ID.
      - Parameter length: 1 to 64.
    type: str
    required: true
  sync_to_storage:
    description:
      - Auto removing the host group from the storage system when a host group
      - is removed. If this parameter is left blank, the default value is false.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def delete_host_group_request_func(host_group_id, param):
        return ansible_base.delete(
            constants.HOSTGROUP_DELETE_URL % host_group_id,
            param)

    result = {}

    try:
        result['data'] = delete(params, delete_host_group_request_func)
        result['msg'] = 'Host group is successfully deleted.'
    except ScriptException as ex:
        result['msg'] = 'Host group fails to be removed. Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        hostgroup_id=dict(required=True, type='str'),
        sync_to_storage=dict(required=False, type='str')
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
