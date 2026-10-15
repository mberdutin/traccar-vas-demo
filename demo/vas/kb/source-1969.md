# issue 1969: Feature Request: Add "Next" / "Previous" navigation buttons to the Time/Period picker

Источник: https://github.com/traccar/traccar-web/issues/1969
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-09-12T04:47:04Z.
Тематические слова: время период часовой пояс свежесть активность

## Текст обращения

### Description
Currently, analyzing data day-by-day or week-by-week requires users to manually open the calendar picker and re-enter the start and end dates/times every single time. If a user wants to audit consecutive days (e.g., checking August 1st, then August 2nd, then August 3rd), it results in a highly repetitive and tedious clicking process.

### Proposal
Add "Next" (Forward) and "Previous" (Backward) arrow buttons next to the period/time selection field.
* Clicking the "Next" button should automatically shift the selected time window forward by its own duration (e.g., if the window is set to 24 hours, clicking "Next" shifts the start and end time exactly 24 hours forward to the next day).
* Clicking "Previous" should shift the window backward by that same duration.

### Benefits
This would drastically streamline the workflow for users who regularly audit logs or travel paths across multiple days, shifting the interface from a manual "click-marathon" to an efficient, user-friendly navigation.


Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
