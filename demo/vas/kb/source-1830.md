# issue 1830: [feature-request] filter devices on map by time

Источник: https://github.com/traccar/traccar-web/issues/1830
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: open; причина закрытия: не указана.
Обновлено в GitHub: 2026-08-01T15:26:20Z.
Тематические слова: фильтр время активность свежесть карта фильтр фильтрация карта список поиск

## Текст обращения

Is it possible to have a feature which allows the devices on map to be filtered by time - e.g.  only show devices which were active within the last 24 hours.


## Комментарий kumarrahul39609-code

Источник: https://github.com/traccar/traccar-web/issues/1830#issuecomment-5152072538

Yeah, totally doable! Here's basically how I'd think about it:

So the main thing you need is some kind of "last active" timestamp on each device, that updates whenever it checks in or sends a location update. Without that there's nothing to actually filter on, so that's step one if it's not already there.

For the actual filtering, you've basically got two options. You could do it server-side, where your backend query just pulls devices where last_active is within the last 24 hours — something like WHERE last_active >= NOW() - INTERVAL '24 hours'. That's more efficient if you've got a ton of devices since you're not even sending data for stuff you're gonna hide anyway.

Or you could do it client-side — pull all the devices with their timestamps once, and then just filter them in the frontend as the user messes with the time window. Feels snappier since you're not re-fetching every time someone changes the filter, but it doesn't scale great if there are thousands of devices.

Honestly a lot of apps just do both — fetch something reasonably bounded from the server (like last 30 days or whatever) and then let the user slice it further on the client.

For the UI, you could do preset buttons or a dropdown (last hour / last 24h / last 7 days / all time), a slider people can drag, or presets plus a custom option with date pickers if you want to get fancy.



function filterDevicesByRecency(devices, hoursThreshold) {
  const cutoff = Date.now() - hoursThreshold * 60 * 60 * 1000;
  r

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
