# Домашнее задание к занятию 6 «Создание собственных модулей»

## Подготовка к выполнению

1. Создайте пустой публичный репозиторий в своём любом проекте: `my_own_collection`.
2. Скачайте репозиторий Ansible: `git clone https://github.com/ansible/ansible.git` по любому, удобному вам пути.
3. Зайдите в директорию Ansible: `cd ansible`.
4. Создайте виртуальное окружение: `python3 -m venv venv`.
5. Активируйте виртуальное окружение: `. venv/bin/activate`. Дальнейшие действия производятся только в виртуальном окружении.
6. Установите зависимости `pip install -r requirements.txt`.
7. Запустите настройку окружения `. hacking/env-setup`.
8. Если все шаги прошли успешно — выйдите из виртуального окружения `deactivate`.
9. Ваше окружение настроено. Чтобы запустить его, нужно находиться в директории `ansible` и выполнить конструкцию `. venv/bin/activate && . hacking/env-setup`.


<details>
    <summary>Вывод консоли:</summary>

```shell
[skvorchenkov@fedora ansible]$ . venv/bin/activate && . hacking/env-setup
running egg_info
creating lib/ansible_core.egg-info
writing lib/ansible_core.egg-info/PKG-INFO
writing dependency_links to lib/ansible_core.egg-info/dependency_links.txt
writing entry points to lib/ansible_core.egg-info/entry_points.txt
writing requirements to lib/ansible_core.egg-info/requires.txt
writing top-level names to lib/ansible_core.egg-info/top_level.txt
writing manifest file 'lib/ansible_core.egg-info/SOURCES.txt'
reading manifest file 'lib/ansible_core.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
warning: no files found matching 'changelogs/CHANGELOG*.rst'
adding license file 'COPYING'
writing manifest file 'lib/ansible_core.egg-info/SOURCES.txt'

Setting up Ansible to run out of checkout...

PATH=/home/skvorchenkov/ansible/bin:/home/skvorchenkov/ansible/venv/bin:/home/skvorchenkov/.local/bin:/home/skvorchenkov/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
PYTHONPATH=/home/skvorchenkov/ansible/test/lib:/home/skvorchenkov/ansible/lib
MANPATH=/home/skvorchenkov/ansible/docs/man:/usr/local/share/man:/usr/share/man

Remember, you may wish to specify your host file with -i

Done!

(venv) [skvorchenkov@fedora ansible]$
```

</details>


Ваша цель — написать собственный module, который вы можете использовать в своей role через playbook. Всё это должно быть собрано в виде collection и отправлено в ваш репозиторий.

**Шаг 1.** В виртуальном окружении создайте новый `my_own_module.py` файл.

**Шаг 2.** Наполните его содержимым:

<details>
    <summary>Содержимое my_own_module.py</summary>

```python
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

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
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
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


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```
</details>

Или возьмите это наполнение [из статьи](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#creating-a-module).

**Шаг 3.** Заполните файл в соответствии с требованиями Ansible так, чтобы он выполнял основную задачу: module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.

- [my_own_module.py](./my_own_module.py)

**Шаг 4.** Проверьте module на исполняемость локально.

```shell
(venv) [skvorchenkov@fedora ansible]$ cat test.json
{
    "ANSIBLE_MODULE_ARGS": {
        "path": "/tmp/testfile.txt",
        "content": "Example text message"
    }
}
(venv) [skvorchenkov@fedora ansible]$ python -m ansible.modules.my_own_module test.json

{"changed": true, "invocation": {"module_args": {"path": "/tmp/testfile.txt", "content": "Example text message"}}}
(venv) [skvorchenkov@fedora ansible]$ cat /tmp/testfile.txt
Example text message
```
**Шаг 5.** Напишите single task playbook и используйте module в нём.

- [single_task_playbook.yml](./playbook/single_task_playbook.yml)

**Шаг 6.** Проверьте через playbook на идемпотентность.

```shell
(venv) [skvorchenkov@fedora ansible]$ ansible-playbook single_task_playbook.yml
[WARNING]: You are running the development version of Ansible. You should only run Ansible from
"devel" if you are modifying the Ansible engine, or trying out features under development. This is a
rapidly changing source of code and can become unstable at any point.
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit
localhost does not match 'all'

PLAY [test my_own_module] ***************************************************************************

TASK [Gathering Facts] ******************************************************************************
ok: [localhost]

TASK [run module] ***********************************************************************************
ok: [localhost]

TASK [dump test output] *****************************************************************************
ok: [localhost] => {
    "msg": {
        "changed": false,
        "failed": false
    }
}

PLAY RECAP ******************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 

```

**Шаг 7.** Выйдите из виртуального окружения.

```shell
(venv) [skvorchenkov@fedora ansible]$ deactivate
[skvorchenkov@fedora ansible]$
```

**Шаг 8.** Инициализируйте новую collection: `ansible-galaxy collection init my_own_namespace.yandex_cloud_elk`.

```shell
[skvorchenkov@fedora ansible]$ ansible-galaxy collection init my_own_namespace.my_own_collection
[WARNING]: You are running the development version of Ansible. You should only run Ansible from
"devel" if you are modifying the Ansible engine, or trying out features under development. This
is a rapidly changing source of code and can become unstable at any point.
- Collection my_own_namespace.my_own_collection was created successfully
```

**Шаг 9.** В эту collection перенесите свой module в соответствующую директорию.

```shell
[skvorchenkov@fedora ansible]$ mkdir my_own_namespace/my_own_collection/plugins/modules
[skvorchenkov@fedora ansible]$ cp ~/ansible/lib/ansible/modules/my_own_module.py ~/ansible/my_own_namespace/my_own_collection/plugins/modules/my_own_module.py
```

**Шаг 10.** Single task playbook преобразуйте в single task role и перенесите в collection. У role должны быть default всех параметров module.

```shell
[skvorchenkov@fedora ansible]$ ansible-galaxy role init single_task_role
[WARNING]: You are running the development version of Ansible. You should only run Ansible from
"devel" if you are modifying the Ansible engine, or trying out features under development. This
is a rapidly changing source of code and can become unstable at any point.
- Role single_task_role was created successfully
[skvorchenkov@fedora ansible]$ cat ~/ansible/my_own_namespace/my_own_collection/roles/single_task_role/tasks/main.yml
---
- name: run module
  my_own_module:
    path: "{{ path }}"
    content: "{{ content }}"
  register: testout
- name: dump test output
  debug:
    msg: '{{ testout }}'
[skvorchenkov@fedora ansible]$ cat ~/ansible/my_own_namespace/my_own_collection/roles/single_task_role/defaults/main.yml
---
path: '/tmp/testfile.txt'
content: 'NEW Example text message. Single Task Role'
```

**Шаг 11.** Создайте playbook для использования этой role.

```shell
[skvorchenkov@fedora ansible]$ cat ~/ansible/my_own_namespace/my_own_collection/playbook/single_task_role.yml
---
- name: Run my_own_module
  hosts: localhost
  roles:
    - single_task_role
```

**Шаг 12.** Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег `1.0.0` на этот коммит.

- [my_own_collection 1.0.0](https://github.com/Mrachneyshiy/my_own_collection/releases/tag/1.0.0)

**Шаг 13.** Создайте .tar.gz этой collection: `ansible-galaxy collection build` в корневой директории collection.

```shell
[skvorchenkov@fedora my_own_collection]$ ansible-galaxy collection build
Created collection for my_own_namespace.my_own_collection at /home/skvorchenkov/ansible/my_own_namespace/my_own_collection/my_own_namespace-my_own_collection-1.0.0.tar.gz
```

**Шаг 14.** Создайте ещё одну директорию любого наименования, перенесите туда single task playbook и архив c collection.

```shell
[skvorchenkov@fedora my_own_collection]$ mkdir ~/example_collection
[skvorchenkov@fedora my_own_collection]$ cp my_own_namespace-my_own_collection-1.0.0.tar.gz ~/example_collection/
[skvorchenkov@fedora playbook]$ cp ~/ansible/single_task_playbook.yml ~/example_collection/
```

**Шаг 15.** Установите collection из локального архива: `ansible-galaxy collection install <archivename>.tar.gz`.

```shell
[skvorchenkov@fedora example_collection]$ ansible-galaxy collection install my_own_namespace-my_own_collection-1.0.0.tar.gz
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'my_own_namespace.my_own_collection:1.0.0' to '/home/skvorchenkov/.ansible/collections/ansible_collections/my_own_namespace/my_own_collection'
my_own_namespace.my_own_collection:1.0.0 was installed successfully
```

**Шаг 16.** Запустите playbook, убедитесь, что он работает.

```shell
[skvorchenkov@fedora example_collection]$ ansible-playbook single_task_playbook.yml
[WARNING]: You are running the development version of Ansible. You should only
run Ansible from "devel" if you are modifying the Ansible engine, or trying out
features under development. This is a rapidly changing source of code and can
become unstable at any point.
[WARNING]: provided hosts list is empty, only localhost is available. Note that
the implicit localhost does not match 'all'

PLAY [test my_own_module] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [run module] **************************************************************
ok: [localhost]

TASK [dump test output] ********************************************************
ok: [localhost] => {
    "msg": {
        "changed": false,
        "failed": false
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 

```

**Шаг 16.** Запустите playbook, убедитесь, что он работает.

Ответ:
- [my_own_collection 1.0.0](https://github.com/Mrachneyshiy/my_own_collection/releases/tag/1.0.0) 
- [my_own_collection-1.0.0.tar.gz](https://github.com/Mrachneyshiy/my_own_collection/blob/main/my_own_namespace-my_own_collection-1.0.0.tar.gz) 

- Выше по пунктам указаны выводы команд.

---
