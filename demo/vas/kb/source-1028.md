# issue 1028: Hourly Based Maintenance is in Milliseconds

Источник: https://github.com/traccar/traccar-web/issues/1028
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-05-10T18:20:07Z.
Тематические слова: уведомления события оповещения

## Текст обращения

On copy of latest master with some customization

**Describe the bug**
Values for Maintenance Start and Period seems to be in milliseconds.

**To Reproduce**
Set device hours to 1
Create new Maintenance Item with "Type" as Hours
Set Maintenance Start to 1
Set Period to 1
Link to device
Create "Maintenance Required" notification
Leave ignition on and you receive a "Maintenance Required" notification in all positions

To Fix:
Set Maintenance Start to 3600000
Set period to 3600000 

After changing to 3600000 it only sends a notification every hour



## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/issues/1028#issuecomment-4416001870

I believe this is already fixed.

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
