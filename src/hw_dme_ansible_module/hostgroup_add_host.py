#!/usr/bin/python
from hw_dme_ansible_core.hostgroup import add_or_remove_host
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: hostgroup_add_host
description:
  - Add hosts to a host group.
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
  host_ids:
    description:
      - Host ID list.
      - Parameter length: 1 to 64.
    type: str
    required: true
  sync_to_storage:
    description:
      - Auto adding the hosts to the host group in the storage system when hosts are added to a host group.
      - If this parameter is left blank, the default value is false.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def group_add_host_func(group_id, param):
        return ansible_base.put(
            constants.ADD_HOST_TO_GROUP_URL % group_id, param)

    result = {}
    try:
        result['data'] = add_or_remove_host(params, group_add_host_func)
        result['msg'] = 'Host is successfully added to host group.'
    except ScriptException as ex:
        result['msg'] = 'Host fails to add to host group. Fault cause: %s.' % ex
        result['failed'] = True

    module.exit_json(**result)


def main():
    argument_spec = dict(
        hostgroup_id=dict(required=True, type='str'),
        host_ids=dict(required=True, type='str'),
        sync_to_storage=dict(required=False, type='str'),
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
