# Календарь-Бот

### Как запустить бота:
Для запуска бота надо запустить файл main.py. Бот почти не использует команды через слеш, всё (кроме запуска через /start) можно делать нажимая на кнопки

### Идея:
Календарь-Бот умеет записывать предстоящие события, показывать и удалять их. Помимо этого бот использует openweathermap.org для того, чтобы показывать погоду на следующую неделю (что может помочь скоректировать планы и т.д.)

### Структура проекта:
Проект поделен на несколько файлов. Основная часть програмы (функции, которые вызывает пользователь) расположена в <b>handlers.py</b>, в <b>kb.py</b> расположены кнопки, классы в <b>states.py</b> служат для того, чтобы обеспечить выполнение одной команды после другой (например, когда мы записываем новое событие, сразу мы кликаем на нужную кнопку, затем бот запрашивает дату, а после ввода даты он запрашивает описания события), в <b>saving_data.py</b> лежит словарь с записанными константами + некоторые константы, в <b>config.py</b> записаны API ключи от телеграм-бота и от openweathermap, а в файле <b>text.py</b> лежат строки, которые мы используем походу выполнения программы

