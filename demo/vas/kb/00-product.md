# VAS Traccar обзор продукта

Срез исходников: 2026-10-15, commit 1f1a5fbb99fb5f8a0ef95ad994090e650c9418df.
Traccar Web — фронтенд GPS-платформы: карта объектов, список устройств,
геозоны, события и отчёты. React, Material UI, Redux и MapLibre. Сервер Traccar
находится в другом репозитории и предоставляет REST API и WebSocket.
Сам фронтенд не определяет координаты по сети оператора и не принимает
протоколы GPS-трекеров: это отдельный backend/integration слой.

Для VAS используем аналогию «диспетчер и автопарк». Это демонстрационная
интерпретация публичного продукта, а не интеграция с реальной сетью МегаФона.
Нужны синтетические устройства и координаты, адаптивный веб-интерфейс.
Нативная сборка iOS/Android в текущую задачу не входит.

Рабочий форк: https://github.com/mberdutin/traccar-vas-demo .
Создавать будущие демо-issues и изменения можно только в этом форке.
Оригинальный traccar/traccar-web — источник знаний и upstream, не адресат
наших учебных запросов. Исходная лицензия Apache-2.0 сохранена в LICENSE.txt.

Источники:
- https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/README.md
- https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/package.json
- https://github.com/traccar/traccar-web/blob/1f1a5fbb99fb5f8a0ef95ad994090e650c9418df/LICENSE.txt
