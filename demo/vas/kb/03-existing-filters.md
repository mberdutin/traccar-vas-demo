# Существующие фильтры карты и списка

На commit 1f1a5fbb99fb5f8a0ef95ad994090e650c9418df уже есть:
фильтр по статусу online/offline/unknown, группам, геозонам и текстовый поиск;
сортировка по имени и lastUpdate. Сортировка lastUpdate не скрывает старые
объекты и не заменяет фильтр «активен за N часов».

В MainPage начальное deviceFilter содержит statuses, groups, geofences.
Отдельный filterMap по умолчанию false: список фильтруется, а карта может
показывать все позиции. Переключатель sharedFilterMap меняет это поведение.
Поэтому требование «одинаковая карта и список» надо согласовать, а не считать
уже существующим свойством.

useFilter.js не содержит порога свежести: текущие условия не сравнивают
lastUpdate или fixTime с now минус выбранный период. Тема из issue 1830
подходит как кандидат на расширение фильтра именно для этого среза.

При уточнении задачи спросить о сочетании со статусами/группами/геозонами,
сохранении периода и сбросе фильтра. Добавление фильтра не должно расширять
список доступных пользователю устройств.

Источники:
- https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/src/main/useFilter.js
- https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/src/main/MainPage.jsx
- https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/src/main/MainToolbar.jsx
- https://github.com/traccar/traccar-web/issues/1830
