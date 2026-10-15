# issue 1570: Traccar Manager on phone does not show detailed traces on active map

Источник: https://github.com/traccar/traccar-web/issues/1570
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-06-20T20:37:00Z.
Тематические слова: позиция координаты местоположение карта

## Текст обращения

Today I have been testing Traccar Manager on android phone. Wanted to follow 2 devices; 1. Traccar Client installed on the same phone to trace my own position. 2. A small device using the H02 protocol to trace my hunting dog.
Some observations: 
The replay function show that both devices upload positions to the Traccar server at demo2.traccar.org as specified and without any glitches. The device time and server time was never more than 2 seconds apart.
**The active map does not show the full, detailed trace** of these devices. To save battery the phone is only unlocked short periods. The positions uploaded in between are not shown when phone is unlocked again. I have found a workaround to keep Traccar Manager alive while screenlock is on. Then many more of the the uploaded positions are shown on the active map. The route tested was 10km. For some areas the active map only show straight lines where there shoud have been a detailed trace. It seem like the download of positions from Traccar server to the Traccar Manager on the phone does not work propery in those areas, even if upload is ok.
For the Traccar Manager to work properly in these situations **the missing positions must be downloaded and shown on the active map**.

## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/issues/1570#issuecomment-3444841068

Why would you expect traces to be downloaded and displayed on the active map?

## Комментарий BardAamodt

Источник: https://github.com/traccar/traccar-web/issues/1570#issuecomment-3446060503

I expect that position that are uploded to the server, as verified with the replay report, also shuld be displayed on the active map?
I see that most/many of them are shown on the active route on the map, but not all.
Even when Traccar Manager is up and running in my 10km test route there are areas where the trace on the active map only show long straight lines instead of the actual route. I suspect the 4G is poor in those areas so that the download of positions from server to TraccarManager on phone does not work properly,  even when the upload to the server is OK with no more than 2 seconds delay according to the replay and postions reports.
When the screensaver has been on to save batteries there is also only a straigt line on the map.
This i not good. The replay shows a detailed trace but only for one device at the time. I need to see both my own and my hunting dogs route on the same screen.

## Комментарий BardAamodt

Источник: https://github.com/traccar/traccar-web/issues/1570#issuecomment-3448566945

I have done a new test today having the Traccar open and running for the whole route. Then I se no glitches in the traces on the active map. So now I believe that there has been no problem with the download of positions from server to TraccarManager due to poor 4G. The main problem remains, that the active map only shows straight lines when the Traccar Manager on phone has been suspended and is not running for some reason. These parts of the traces should have been refreshed, either automatically or by some button to press.

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
