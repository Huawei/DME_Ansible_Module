#!/usr/bin/python
from hw_dme_ansible_core.host import delete
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: host_remove
description:
  - Remove a host.
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
  sync_to_storage:
    description:
      - Auto removing the host from the storage system when a host is removed.
      - If this parameter is left blank, the default value is false.
    type: str
    required: true
'''


def run_module(params, ansible_base, module):
    def host_delete_request_func(host_id, param):
        return ansible_base.delete(constants.HOST_DELETE_URL % host_id, param)

    result = {}
    try:
        result['data'] = delete(params, host_delete_request_func)
        result['msg'] = 'Host is successfully removed.'
    except ScriptException as ex:
        result['msg'] = 'Host fails to be removed. Fault cause: %s.' % ex
        result['failed'] = True

    module.exit_json(**result)


def main():
    argument_spec = dict(
        host_id=dict(required=True, type='str'),
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
