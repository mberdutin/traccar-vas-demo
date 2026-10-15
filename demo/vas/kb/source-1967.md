# issue 1967: POI layer is rendered above device markers and can obscure them

Источник: https://github.com/traccar/traccar-web/issues/1967
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-09-08T13:21:43Z.
Тематические слова: позиция координаты местоположение карта

## Текст обращения

Describe the bug
The POI layer is rendered above device markers on the main map.

When the POI layer contains tracks or routes (for example a KML file with line geometries), the lines can visually cover device markers that are located on the same route. This makes live tracking difficult because the tracked devices become partially or completely obscured by the POI layer.

To reproduce

Configure a KML file as the poiLayer.
Add one or more line tracks/routes to the KML.
Display a device whose position is located on one of those lines.
Observe that the POI layer is rendered above the device marker.

Expected behavior
Device markers should always be rendered above the POI layer.

Current behavior
The POI layer can be added after the device marker layers and therefore appears above them.

Technical details
In MainMap.jsx, moving <PoiMap /> before <MapPositionMarkers /> is not sufficient because the POI data is loaded asynchronously.

PoiMap initially has no data and its layers are enabled only after the KML fetch completes. At that point the POI MapLibre layers are added after the device marker layers and therefore appear above them.

I tested a fix where:

PoiMap is mounted before MapPositionMarkers
the POI layer is created immediately using an empty FeatureCollection
the layer remains enabled
the KML data updates the existing source instead of causing the layer to be recreated

This keeps the POI layer below the device markers and works correctly in live tracking.

Version
Traccar Web 6.15.3

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
