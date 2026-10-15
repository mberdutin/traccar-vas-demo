# issue 1338: MapView recreating controls, losing state and jumping map on style change

Источник: https://github.com/traccar/traccar-web/issues/1338
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-06-20T21:03:00Z.
Тематические слова: позиция координаты местоположение карта

## Текст обращения

**Describe the bug**
MapView.jsx removes and re-adds all it's children when the map style changes and mapReady flips. This reinitializes all the children causing their state to be lost - for MapDefaultCamera for example this causes it to jumpto the default map location again when you change map style - exactly where it jumps depends on whether there is a selected position. Children just need to be aware of the chane and that they need to re-add and map layers and sources.

It is triggered by having this line in MapView.jsx ln123
`{mapReady && children}`

**To Reproduce**
Steps to reproduce the behaviour:
1. Go to the main map page
2. Select a tracker
3. Pan the map to a different location
4. Change the map style
5. Watch the map jump to the default location again rather than staying where it was


A potential fix is here
https://github.com/paul-777/traccar-web/tree/MapviewSubControlsLifecycle


## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/issues/1338#issuecomment-2730396640

Is jumping the only issue?

## Комментарий paul-777

Источник: https://github.com/traccar/traccar-web/issues/1338#issuecomment-2732571954

Jumping is the most significant/obvious from a user perspective and one I find very irritating. But I actually found the issue when prototyping something similar to the POI layer and found that every time the map style changed the component re-fetched it's data. Looking at the code I think the PoiMap would do the same. IMO having the children get recreated when changing map style is rather obscure unexpected behaviour that can lead to some difficult to diagnose issues when developing components.
(Thanks for such a great product!)

## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/issues/1338#issuecomment-2732921794

I don't think it's obscure. It is a very clean way to handle map re-initialization. Otherwise you would have to think about in every single sub-component. Is it possible to have some kind of opt-in option for children?

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
