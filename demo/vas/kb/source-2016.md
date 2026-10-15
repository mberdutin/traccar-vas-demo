# pull_request 2016: Support placemark icons in POI layer

Источник: https://github.com/traccar/traccar-web/pull/2016
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: не указана.
Обновлено в GitHub: 2026-10-08T16:49:46Z.
Тематические слова: изменение реализация фильтр merged PR

## Текст обращения

The POI layer (`map.poi`) parses KML with togeojson, which already extracts each placemark's `<IconStyle><Icon><href>` into the `icon` property, but the layer only draws circles, so icons in a POI file are ignored.

This draws the icon for placemarks that define one:

- each distinct icon URL is loaded once and registered with the map
- placemarks with a loaded icon are drawn by a new symbol layer (honouring `<IconStyle><scale>`), with the title raised above the icon
- placemarks without an icon, or whose icon fails to load, keep the existing circle, so current POI files render exactly as before

Icons are loaded with `crossOrigin = 'anonymous'`, so an icon hosted on another origin needs to send `Access-Control-Allow-Origin`, the same requirement the KML file itself already has.

Tested with a POI file mixing an icon placemark, a plain placemark and an icon URL that returns 404: the first draws its icon, the other two draw circles.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/pull/2016#issuecomment-6008160376

Please provide screenshot before and after. And attach the POI file you used for testing.

## Комментарий zaepho

Источник: https://github.com/traccar/traccar-web/pull/2016#issuecomment-6009375570

Updated per the review: ee5f480.

Same POI file and view, on 6.16.0.

**Before (stock)**

![before](https://github.com/zaepho/traccar-web/raw/pr-2016-assets/before.png)

**After (this PR)**

![after](https://github.com/zaepho/traccar-web/raw/pr-2016-assets/after.png)

Test file: [poi-test.kml](https://github.com/zaepho/traccar-web/blob/pr-2016-assets/poi-test.kml), with its icon at [icon.svg](https://github.com/zaepho/traccar-web/blob/pr-2016-assets/icon.svg) (the KML expects it at `http://localhost:18090/icon.svg`). Placemarks:

- **Icon**: icon with `<scale>0.5</scale>`
- **Large icon**: the same icon, unscaled
- **Dot**: no icon
- **Broken icon**: icon URL that returns 404 (falls back to the circle)
- **Area** / **Route**: a polygon and a line; their vertices draw exactly as before

## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/pull/2016#issuecomment-6018449963

Can you please remove all the comments.

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
