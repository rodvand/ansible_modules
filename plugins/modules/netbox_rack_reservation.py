#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Martin Rødvand (@rodvand)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_rack_reservation
short_description: Create, update or delete racks reservations within NetBox
description:
  - Creates, updates or removes racks from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Martin Rødvand (@rodvand)
requirements:
  - pynetbox
version_added: '3.21.0'
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    type: dict
    description:
      - Defines the rack reservation
    suboptions:
      rack:
        description:
          - The rack
        required: true
        type: str
      units:
        description:
          - The units in the rack
        required: true
        type: list
        elements: raw        
      user:
        description:
          - Required if I(state=present) and the rack reservation does not exist yet
        required: false
        type: raw
      tenant:
        description:
          - The tenant that the rack reservation will be assigned to
        required: false
        type: raw      
      location:
        description:
          - The location the rack reservation will be associated to
        required: false
        type: raw             
      description:
        description:
          - Description of the rack reservation
        required: true
        type: str        
      comments:
        description:
          - Comments that may include additional information in regards to the rack reservation
        required: false
        type: str
      tags:
        description:
          - Any tags that the rack reservation may need to be associated with
        required: false
        type: list
        elements: raw
      custom_fields:
        description:
          - must exist in NetBox
        required: false
        type: dict
    required: true
"""

EXAMPLES = r"""
- name: "Test NetBox modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create rack reservation
      netbox.netbox.netbox_rack_reservation:
        data:
          rack: Test rack
          units:
            - 1
            - 3
            - 5
          description: Patch panels
        state: present

    - name: Delete rack reservation within netbox
      netbox.netbox.netbox_rack_reservation:
        data:
          rack: Test Rack
          description: Patch panels
        state: absent
"""

RETURN = r"""
rack_reservation:
  description: Serialized object as created or already existent within NetBox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_dcim import (
    NetboxDcimModule,
    NB_RACK_RESERVATIONS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    rack=dict(required=True, type="str"),
                    units=dict(required=False, type="list", elements="raw"),
                    user=dict(required=False, type="raw"),
                    tenant=dict(required=False, type="raw"),
                    location=dict(required=False, type="raw"),
                    description=dict(required=True, type="str"),
                    comments=dict(required=False, type="str"),
                    tags=dict(required=False, type="list", elements="raw"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["rack", "description"]),
        ("state", "absent", ["rack", "description"]),
    ]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_rack_reservation = NetboxDcimModule(module, NB_RACK_RESERVATIONS)
    netbox_rack_reservation.run()


if __name__ == "__main__":  # pragma: no cover
    main()
