# Python. Лабораторная работа 2  
### Bash (Easy+Medium)

- **Библиотеки:**
    - `pathlib` — _Работа с путями_
    - `shutil` — _Файловые операции_
    - `shlex` – _Парсинг команд_
    - `readline` – _Автокомплит_
    - `logging` — _Запись всех действий в shell.log_
    - `json` — _Сохранение истории команд между сессиями_
    - `colorama` – _Цветной ввод_
    - `dataclass`, `enum`, `abc`
      
- **Интересные штучки:**
    - Поддержка [автокомплита](./src/terminal/autocomplete.py) _(чуть корявая)_
    - `.trash` папка создаётся в `cwd`
    - Очень легко добавляются кастомные команды (см. [лаб. 3]()):
      - Необходимо просто создать и реализовать класс от [`BashCommand`](./src/terminal/command.py) (или [`UndoableBashCommand`](./src/commands/custom_abc/undoable_command.py))
        
      > `UndoableBashCommand`, [`ArchiveBashCommand`](./src/commands/custom_abc/archive_command.py): ABC наследники от `BashCommand` – можно реализовывать свои abc по этому принципу

    - Есть возможность добавить полную поддержку _windows_:
      - Над pathlib реализована абстракция [`FS`](./src/terminal/file_system/fs.py).
      - Все команды обращаются к ней.
      - Возможна подмена инстанса `fs` на кастомный класс, наследованный от `FS`.
    - Вывод из команды `tuple[list[BashError], str]]`:
      - `list[BashError]` – список ошибок, которые не прерывают исполнение команды (случаи с `ls dir1 dir2`), но сообщение о них логгируются и выводятся
      - `str` – строка, которую необходимо напечатать (вывод команды)
      - [`PrintBuilder`](./src/utils/print_builder.py) – кастомный класс, который облегчает создание одного `str` для принта нескольких строк. (`PrintBuilder.get() -> str`)
      - Если есть ошибка, которая прерывает исполнение команды, то вызывается обычный `raise`

### Что нового я познал?
- Каково быть единорогом
- Научился работать с `pathlib`, `shutil`, `shlex` и `logging`
- Написал кастомный [декоратор](./src/terminal/file_system/resolve_path.py), который работает с методами и функциями (проверяет сигнатуру через `inspect`)

## Структура проекта
```
bash
├── src
│   ├── terminal
│   │   ├── file_system
│   │   │   ├── fs.py						# Обёртка над FS для операций с файловой системой
│   │   │   ├── fs_properties.py			# Проверка свойств Path
│   │   │   └── ...
│   │   ├── autocomplete.py					# Автодополнение ввода в терминале
│   │   ├── command.py						# Родительский класс для всех команд терминала
│   │   ├── terminal.py						# Основной цикл ввода, разбор и выполнение команд, инициализация среды
│   │   └── history.py						# Singleton: управление историей
│   ├── commands
│   │   ├── import_default_commands.py		# Импорт всех *_command.py из подпапок
│   │   ├── custom_abc						# archive, unarchive, undoable
│   │   ├── archive							# zip, unzip, tar, untar
│   │   ├── files_content					# cat, grep
│   │   ├── history							# history, undo
│   │   ├── navigation						# cd, ls
│   │   └── undoables						# cp, mv, rm
│   ├── core
│   │   ├── config.py						# Настройки проекта: имена файлов, флаги поведения
│   │   ├── errors.py						# Кастомные ошибки
│   │   └── logging.py						# Инициализация логгера, функция log()
│   ├── utils
│   │   ├── print_builder.py				# Многострочный вывод в строку
│   │   ├── could_be_undo.py				# Проверка, можно ли отменить запись из истории
│   │   └── ...
│   └── main.py								# Входная точка в программу
└── tests									# Тесты для команд
```
