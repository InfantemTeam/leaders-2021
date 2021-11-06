# Лидеры цифровой трансформации 2021

by InfantemTeam \<infantemteam@sdore.me>.

## Результаты работы модели
> ### [result_task.csv](/tree/master/result_task.csv)


## Тестовый инстанс
> ### https://leaders.sdore.me
### Тестовая страница для проверки рекомендаций: [/test](https://leaders.sdore.me/test) (на сайте нет ссылки сюда).


## Установка
Автоматически подготовит виртуальную среду (virtualenv) и подтянет зависимости:
> ```console
> $ ./init.sh
> ```


## Запуск
Способ запуска стандартный для Quart.
* **Dev (`dev.sh`):**
  > ```console
  > $ PYTHONPATH=.. python3 -m ${PWD##*/}
  > ```
  (сервер запустится на unix-сокете `/tmp/leaders.sock`.)
* **Prod (`prod.sh`):**
  > Через любой ASGI-совместимый сервер, например:
  > ```console
  > $ PYTHONPATH=.. hypercorn ${PWD##*/}.app:app
  > ```

  _(имя директории, содержащей данный репозиторий, должно быть валидным идентификатором Python, т.е., в частности, без `-`)._

Файл базы данных SQLite (`db.sqlite`) будет создан в текущей директории.


## Получение рекомендаций
- [/api/recomms](https://leaders.sdore.me/api/recomms)?user\_id=N&count=M — API (JSON)
- [/test](https://leaders.sdore.me/test) — Admin
- [/lk](https://leaders.sdore.me/lk) — User
