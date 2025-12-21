//https://github.com/sennett-lau/readme-project-structure-generator.git
export const projectStructure = {

        src: {
            terminal: {
                file_system: {
                    'fs.py': 'Обёртка над FS для операций с файловой системой',
                    'fs_properties.py': 'Проверка свойств Path',
                    '...': ''
                },
                'autocomplete.py': 'Автодополнение ввода в терминале',
                'command.py': 'Родительский класс для всех команд терминала',
                'terminal.py': 'Основной цикл ввода, разбор и выполнение команд, инициализация среды',
                'history.py': 'Singleton: управление историей'
            },
            commands: {
                'import_default_commands.py': 'Импорт всех *_command.py из подпапок',
                'custom_abc': 'archive, unarchive, undoable',
                'archive': 'zip, unzip, tar, untar',
                'files_content': 'cat, grep',
                'history': 'history, undo',
                'navigation': 'cd, ls',
                'undoables': 'cp, mv, rm'
            },
            core:{
                'config.py': 'Настройки проекта: имена файлов, флаги поведения',
                'errors.py': 'Кастомные ошибки',
                'logging.py': 'Инициализация логгера, функция log()'
            },
            utils: {
                'print_builder.py': 'Многострочный вывод в строку',
                'could_be_undo.py': 'Проверка, можно ли отменить запись из истории',
                '...': ''
            },
            'main.py': 'Входная точка в программу',
        },
        'tests': 'Тесты для команд'


}
