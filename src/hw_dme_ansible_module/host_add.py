#!/usr/bin/python
from hw_dme_ansible_core.host import add
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: host_add
description:
  - Add a host.
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
  access_mode:
    description:
      - Host addition mode.
      - Value range:
        - NONE (no authentication).
    type: str
    required: true
  type:
    description:
      - Displayed status.
      - Value range:
        - UNKNOWN
        - LINUX
        - WINDOWS
        - SUSE
        - EULER
        - REDHAT
        - CENTOS
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
    required: true
  host_name:
    description:
      - Host name.
      - Parameter length: 1 to 255.
    type: str
    required: false
  description:
    description:
      - Host description.
      - Parameter length: 0 to 63.
    type: str
    required: false
  iSCSI_initiator:
    description:
      - iSCSI initiator list.
      - Parameter length: 1 to 223.
    type: str
    required: false
  FC_initiator:
    description:
      - FC initiator list.
      - Parameter length: 1 to 223.
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
      - Parameter length: 1 to 64.
    type: str
    required: false
  sync_to_storage:
    description:
      - Auto synchronizing information about added hosts to the storage system,
      - including the host name, IP address, and initiator list.
      - The default value is false.
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
      - Initiator path type.
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
        - and mode_three
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def host_add_request_func(param):
        return ansible_base.post(constants.HOST_ADD_URL, param)

    result = {}
    try:
        result['data'] = add(params, host_add_request_func)
        result['msg'] = 'Host is successfully added.'
    except ScriptException as ex:
        result['msg'] = 'Host fails to be added. Fault cause: %s.' % ex
        result['failed'] = True

    module.exit_json(**result)


def main():
    argument_spec = dict(
        access_mode=dict(required=True, type='str'),
        type=dict(required=True, type='str'),
        host_name=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        iSCSI_initiator=dict(required=False, type='str'),
        FC_initiator=dict(required=False, type='str'),
        azs=dict(required=False, type='str'),
        project_id=dict(required=False, type='str'),
        sync_to_storage=dict(required=False, type='str'),
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
