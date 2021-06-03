# -*- coding: utf-8
from hw_dme_ansible_core.volume import modify
from hw_dme_ansible_core.ansible_base import AnsibleBase
from hw_dme_ansible_core.common import ScriptException
from hw_dme_ansible_core import constants
from ansible.module_utils.basic import AnsibleModule
from hw_dme_ansible_core.ansible_base import ARGUMENT_SPEC_BASE

DOCUMENTATION = r'''
---
module: lun_modify
description:
  - Modify a specified LUN.
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
  volume_wwn:
    description:
      - LUN WWN.
      - Parameter length of each WWN: 1 to 64.
    type: str
    required: true
  name:
    description:
      - New LUN name.
      - Parameter length: 1 to 255.
    type: str
    required: false
  description:
    description:
      - LUN description modification.
    type: str
    required: false
  owner_controller:
    description:
      - Owning controller.
      - Parameter length: 1 to 255.
    type: str
    required: false
  prefetch_policy:
    description:
      - Prefetch policy.
      - Value range:
        - 0 (no prefetch)
        - 1 (constant prefetch)
        - 2 (variable prefetch)
        - 3 (intelligent prefetch)
    type: str
    required: false
  prefetch_value:
    description:
      - Prefetch policy value.
    type: str
    required: false
  smarttier:
    description:
      - Data relocation policy. The default value is no relocation.
      - Value range:
        - 0 (no relocation)
        - 1 (automatic relocation)
        - 2 (relocation to the high-performance layer)
        - 3 (relocation to the low-performance layer)
    type: str
    required: false
  maxbandwidth:
    description:
      - QoS attribute – Maximum bandwidth.
    type: str
    required: false
  maxiops:
    description:
      - QoS attribute – Maximum IOPS.
    type: str
    required: false
  minbandwidth:
    description:
      - QoS attribute – Minimum bandwidth.
    type: str
    required: false
  miniops:
    description:
      - QoS attribute – Minimum IOPS.
    type: str
    required: false
  control_policy:
    description:
      - QoS attribute – Control policy
      - Value range:
        - 0 (protecting the lower limit of I/Os)
        - 1 (controlling the upper limit of I/Os)
    type: str
    required: false
  latency:
    description:
      - QoS attribute – Latency.
    type: str
    required: false
  qos_enabled:
    description:
      -  Enabling SmartQoS.
    type: str
    required: false
'''


def run_module(params, ansible_base, module):
    def modify_luns_request_func(volume_id, param):
        return ansible_base.put(constants.LUN_MODIFY_URL % volume_id, param)

    result = {}
    try:
        result['data'] = modify(params, modify_luns_request_func,
                                ansible_base.task_request,
                                ansible_base.lun_id_convert_func)
        result['msg'] = 'Modify LUN successfully.'
    except ScriptException as ex:
        result['msg'] = 'Modify LUN failed, Fault cause: %s.' % ex
        result['failed'] = True
    module.exit_json(**result)


def main():
    argument_spec = dict(
        volume_wwn=dict(required=True, type='str'),
        name=dict(required=False, type='str'),
        description=dict(required=False, type='str'),
        owner_controller=dict(required=False, type='str'),
        prefetch_policy=dict(required=False, type='str'),
        prefetch_value=dict(required=False, type='str'),
        smarttier=dict(required=False, type='str'),
        maxbandwidth=dict(required=False, type='str'),
        maxiops=dict(required=False, type='str'),
        minbandwidth=dict(required=False, type='str'),
        miniops=dict(required=False, type='str'),
        control_policy=dict(required=False, type='str'),
        latency=dict(required=False, type='str'),
        qos_enabled=dict(required=False, type='str')
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
