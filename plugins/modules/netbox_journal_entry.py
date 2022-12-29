#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_ip_address
short_description: Creates or removes IP addresses from NetBox
description:
  - Creates or removes IP addresses from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
  - Anthony Ruhier (@Anthony25)
requirements:
  - pynetbox
version_added: '0.1.0'
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    type: dict
    description:
      - Defines the journal entry
    suboptions:
      created_by:
        description:
          - The user creating the journal entry. Omit to use the API token user
        required: false
        type: int        
      kind:
        description:
          - The kind of journal entry
        required: false
        type: str      
      assigned_object_id:
        description:
          - ID of the object to create the journal entry on
        required: true
        type: int
      assigned_object_type:
        description:
          - The object type of the model
        required: true
        type: str
      comments:
        description:
          - The comment associated with the journal entry
        required: true
        type: str
      tags:
        description:
          - Any tags that the IP address may need to be associated with
        required: false
        type: list
        elements: raw
      custom_fields:
        description:
          - must exist in NetBox
        required: false
        type: dict
    required: true
  state:
    description:
      - |
        Use C(present), C(new) or C(absent) for adding, force adding or removing.
        C(present) will check if the IP is already created, and return it if
        true. C(new) will force to create it anyway (useful for anycasts, for
        example).
    choices: [ absent, new, present ]
    default: present
    type: str
"""

EXAMPLES = r"""
- name: "Test NetBox IP address module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create IP address within NetBox with only required information
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          address: 192.168.1.10
        state: present

    - name: Force to create (even if it already exists) the IP
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          address: 192.168.1.10
        state: new

    - name: Get a new available IP inside 192.168.1.0/24
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          prefix: 192.168.1.0/24
        state: new

    - name: Delete IP address within netbox
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          address: 192.168.1.10
        state: absent

    - name: Create IP address with several specified options
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          address: 192.168.1.20
          vrf: Test
          tenant: Test Tenant
          status: Reserved
          role: Loopback
          description: Test description
          tags:
            - Schnozzberry
        state: present

    - name: Create IP address and assign a nat_inside IP
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          address: 192.168.1.30
          vrf: Test
          nat_inside:
            address: 192.168.1.20
            vrf: Test
          interface:
            name: GigabitEthernet1
            device: test100

    - name: Ensure that an IP inside 192.168.1.0/24 is attached to GigabitEthernet1
      netbox.netbox.netbox_ip_address:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          prefix: 192.168.1.0/24
          vrf: Test
          interface:
            name: GigabitEthernet1
            device: test100
        state: present    
"""

RETURN = r"""
journal_entry:
  description: Serialized object as created or already existent within NetBox
  returned: on creation
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
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_extras import (
    NetboxExtrasModule,
    NB_JOURNAL_ENTRIES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec["state"] = dict(required=False, default="new", choices=["new"])
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    created_by=dict(required=False, type="int"),
                    kind=dict(required=False, type="raw"),
                    assigned_object_type=dict(required=False, type="str"),
                    assigned_object_id=dict(required=False, type="str"),
                    comments=dict(required=False, type="str"),                    
                    tags=dict(required=False, type="list", elements="raw"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )

    required_if = [
        (
            "state",
            "new",
            ["comments", "assigned_object_type", "assigned_object_id"],
            True,
        ),
    ]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    netbox_journal_entry = NetboxExtrasModule(module, NB_JOURNAL_ENTRIES)
    netbox_journal_entry.run()


if __name__ == "__main__":  # pragma: no cover
    main()
