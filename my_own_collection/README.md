# Ansible Collection - my_own_namespace.my_own_collection

Documentation for the collection.

- my_own_collection
  - my_own_module.py
  - single_task_role

Коллекция запускает модуль, который с помощью task_role создает текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.
