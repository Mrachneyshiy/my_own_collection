#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_module_create_file
short_description: This is module creates a text file
description:
    Module creates a text file on the remote host at the path specified by the `path` parameter, with the content specified by the `content` parameter
options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
version_added: "1.0.0"
author:
    - t585585
'''

EXAMPLES = r'''
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='Example text')
    )

    result = dict(
        changed=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.check_mode:
        module.exit_json(**result)

    if not(os.path.exists(module.params['path'])
    and os.path.isfile(module.params['path'])
    and open(module.params['path'],'r').read() == module.params['content']):
        try:
            with open(module.params['path'], 'w') as file:
                file.write(module.params['content'])
                result['changed'] = True
        except Exception as exp:
            module.fail_json(msg=f"Something gone wrong: {exp}", **result)

    if module.params['path'] == 'fail me':
        module.fail_json(msg='This is a fail', **result)
    module.exit_json(**result)

def main():
    run_module()
if __name__ == '__main__':
    main()
