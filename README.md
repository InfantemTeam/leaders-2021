# Лидеры цифровой трансформации 2021

by InfantemTeam \<infantemteam@sdore.me>.


## Тестовый инстанс
> ### https://leaders.sdore.me


## Установка
Автоматически подготовит виртуальную среду (virtualenv) и подтянет зависимости:
> ```shell-session
> $ ./init.sh
> ```


## Запуск
Способ запуска стандартный для Quart.
* **Dev (`dev.sh`):**
  > ```shell-session
  > $ PYTHONPATH=.. python3 -m ${PWD##*/}
  > ```
  (сервер запустится на unix-сокете `/tmp/leaders.sock`.)
* **Prod (`prod.sh`):**
  > Через любой ASGI-совместимый сервер, например:
  > ```shell-session
  > $ PYTHONPATH=.. hypercorn ${PWD##*/}.app:app
  > ```

  _(имя директории, содержащей данный репозиторий, должно быть валидным идентификатором Python, т.е., в частности, без `-`)._

Файл базы данных SQLite (`db.sqlite`) будет создан в текущей директории.
