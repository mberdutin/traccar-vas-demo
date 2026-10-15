# issue 1757: Title: Report filter device/group selection broken — Cannot read properties of null (reading 'focus')

Источник: https://github.com/traccar/traccar-web/issues/1757
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-04-17T04:04:10Z.
Тематические слова: фильтр фильтрация карта список поиск

## Текст обращения

Steps to reproduce

1. Navigate to any report page (e.g. Events, Trips, Stops)
2. Click on the Devices or Groups selection field

Expected behavior

A dropdown appears listing available devices or groups.

Actual behavior

The dropdown does not open. The following error is thrown in the console:


Uncaught TypeError: Cannot read properties of null (reading 'focus')
    at handleClick (useAutocomplete-DY0MiNdP.js:623:20)
Full stack trace points to SelectField.jsx → ReportFilter.jsx → EventReportPage.jsx.


@mui/material: 9.0.0
React: 19.2.5
Browser: Chrome

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
