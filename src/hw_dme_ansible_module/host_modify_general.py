#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE
from hw_dme_ansible_core import constants
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core.host import update_general

DOCUMENTATION = r'''
---
module: host_modify_general
description:
  - Modify basic host information.
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
      - IP address for adding the host.
      - Parameter length: 0 to 127.
    type: str
    required: false
  host_name:
    description:
      - Host name.
      - Parameter length: 1 to 255.
    type: str
    required: false
  os_type:
    description:
      - Host type.
      - Value range:
        - LINUX
        - WINDOWS
        - WINDOWSSERVER2012
        - SOLARIS
        - HPUX
        - AIX
        - XENSERVER
        - MACOS
        - VMWAREESX
        - ORACLE
        - OPENVMS
        - ORACLE_VM_SERVER_FOR_X86
        - ORACLE_VM_SERVER_FOR_SPARC
    type: str
    required: false
  azs:
    description:
      - AZ ID list.
      - Parameter length: 1 to 64.
    type: str
    required: false
  project_id:
    description:
      - Project ID.
      - Parameter length: 0 to 64.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def host_update_request_func(host_id, param):
        return ansible_base.put(constants.HOST_MODIFY_GENERAL_URL % host_id,
                                param)

    result = {}
    try:
        result['data'] = update_general(params, host_update_request_func)
        result['msg'] = 'Host is successfully updated.'
    except ScriptException as ex:
        result['msg'] = 'Host fails to be updated. Fault cause: %s.' % ex
        result['failed'] = True

    module.exit_json(**result)


def main():
    argument_spec = dict(
        host_id=dict(required=True, type='str'),
        ip=dict(required=False, type='str'),
        host_name=dict(required=False, type='str'),
        os_type=dict(required=False, type='str'),
        azs=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
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
