# Карта компонентов фронтенда Traccar

Состояние на commit 1f1a5fbb99fb5f8a0ef95ad994090e650c9418df.

- src/main/MainPage.jsx: выбранное устройство, позиции и фильтры; разделение
  desktop/mobile; передача отфильтрованных данных карте и списку.
- src/main/MainToolbar.jsx: поля фильтра статусов, групп и геозон, сортировка,
  переключатель применения фильтра к карте.
- src/main/useFilter.js: общий расчёт отфильтрованных устройств и позиций;
  поиск по имени, uniqueId, телефону, модели и контакту, сортировка lastUpdate.
- src/main/DeviceList.jsx и DeviceRow.jsx: виртуализированный список и строка
  устройства, загрузка /api/devices, отображение статуса.
- src/SocketController.jsx: обновления через WebSocket и события приложения.
- src/common/util/usePersistedState.js: сохранение состояния в localStorage.
- src/common/components/PositionValue.jsx: представление полей позиции.
- src/resources/l10n: переводы; новые подписи UI требуют локализации.
- vite.config.js: dev-server 3000, прокси API/WebSocket к localhost:8082,
  production build в build/.

Это ориентиры для постановки и исследования. Перед изменением кода разработчик
проверяет актуальный checkout: карта относится к указанному SHA.

Источник дерева и файлов:
https://github.com/traccar/traccar-web/tree/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/src
https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/vite.config.js
