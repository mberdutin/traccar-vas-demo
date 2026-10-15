# issue 1849: Feature Request: Implement Per-Device Log View in Status Card

Источник: https://github.com/traccar/traccar-web/issues/1849
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: open; причина закрытия: не указана.
Обновлено в GitHub: 2026-08-16T03:45:05Z.
Тематические слова: фильтр фильтрация карта список поиск время период часовой пояс свежесть активность

## Текст обращения

**Description**
Currently, the web-based log view in Traccar provides a global stream of data from all connected devices. While useful for general system monitoring, this approach is inefficient for targeted troubleshooting, as it requires users to manually parse through high-volume traffic to isolate logs for a specific unit.

I propose the integration of a dedicated "Device Log" terminal within the individual device status card. When triggered, this view should open a log terminal filtered to display data exclusively for that device.

**Proposed Solution**
Add a "Terminal" button or link to the device status card.
Upon clicking, initiate a log stream that automatically applies a filter based on the device ID or unique identifier.
This will allow technicians to verify packet reception, identify protocol errors, and troubleshoot connectivity issues in real-time without the noise of the global log stream.

**Demo**
The following video demonstrates the implementation:

https://github.com/user-attachments/assets/4c55c32f-5302-43de-884b-d13a54b088e1

**Additional Information**
As seen in the demo the terminal link is only active on the main map page, the terminal also has filter(the search), pause/play, clear, copy and download feature.
I can send a PR if the community is interested in this.

## Комментарий hiSandog

Источник: https://github.com/traccar/traccar-web/issues/1849#issuecomment-4912052557

The scope would be easier to review if the first version defined a small acceptance contract for `Feature Request: Implement Per-Device Log View in Status Card`. I would call out the default behavior, the migration/backwards-compatibility story, and one or two cases that are intentionally out of scope so the implementation does not grow beyond the original request.


## Комментарий hypoclone

Источник: https://github.com/traccar/traccar-web/issues/1849#issuecomment-4917128801

> The scope would be easier to review if the first version defined a small acceptance contract for `Feature Request: Implement Per-Device Log View in Status Card`. I would call out the default behavior, the migration/backwards-compatibility story, and one or two cases that are intentionally out of scope so the implementation does not grow beyond the original request.

Thanks for the suggestion. The video demo already reflects the intended default behavior: the Terminal action is available from the device status card on the main map page, opens the existing terminal UI, and automatically applies a filter for the selected device. The implementation reuses the existing log streaming infrastructure, so there are no API, database, or migration changes, and the existing global log view remains unchanged. For the initial implementation, the scope is limited to exposing a per-device filtered view of the existing log stream; features such as historical log playback or multi-device log sessions are intentionally out of scope.

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
