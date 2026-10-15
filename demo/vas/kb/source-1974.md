# pull_request 1974: Bump maplibre-gl from 6.7.0 to 6.8.0

Источник: https://github.com/traccar/traccar-web/pull/1974
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: не указана.
Обновлено в GitHub: 2026-09-11T00:41:40Z.
Тематические слова: изменение реализация фильтр merged PR

## Текст обращения

Bumps [maplibre-gl](https://github.com/maplibre/maplibre-gl-js) from 6.7.0 to 6.8.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/maplibre/maplibre-gl-js/releases">maplibre-gl's releases</a>.</em></p>
<blockquote>
<h2>v6.8.0</h2>
<h3>✨ Features and improvements</h3>
<ul>
<li>Add <code>map.getStyleUrl()</code>, which returns the URL the style was loaded from, or <code>null</code> when the style was given as an object (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/7109">#7109</a>) (by <a href="https://github.com/bradymadden97"><code>@​bradymadden97</code></a> and <a href="https://github.com/giswqs"><code>@​giswqs</code></a>)</li>
<li>Sample terrain render-to-texture output through mipmaps with trilinear filtering, so draped layers stop shimmering and aliasing at high pitch (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8328">#8328</a>, continues <a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/7673">#7673</a>) (by <a href="https://github.com/AveryanAlex"><code>@​AveryanAlex</code></a>)</li>
<li>Build the <code>Intl.Segmenter</code> instances used for text shaping on first use instead of at import, shaving several milliseconds off loading MapLibre on the main thread (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8337">#8337</a>) (by <a href="https://github.com/cherenkov"><code>@​cherenkov</code></a>)</li>
<li>Link shader programs before reading their compile status, so the driver can overlap the compiles and the main thread waits less on shader compilation (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8338">#8338</a>) (by <a href="https://github.com/cherenkov"><code>@​cherenkov</code></a>)</li>
<li>Build the default <code>Marker</code> pin once and clone it per marker, so creating many default markers takes roughly half the constructor time (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8340">#8340</a>) (by <a href="https://github.com/cherenkov"><code>@​cherenkov</code></a>)</li>
<li>Add SDF rendering support for fill patterns, using <code>fill-color</code> as the foreground color (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/7747">#7747</a>) (by <a href="https://github.com/bradymadden97"><code>@​bradymadden97</code></a> and <a href="https://github.com/deniial00"><code>@​deniial00</code></a>)</li>
<li>Warn once when the canvas is clamped to <code>maxCanvasSize</code>, which previously lowered the rendered resolution silently (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/8200">#8200</a>) (by <a href="https://github.com/str0kes"><code>@​str0kes</code></a>)</li>
</ul>
<h3>🐞 Bug fixes</h3>
<ul>
<li>Fix a marker's popup jumping to another world copy when the marker is moved across the antimeridian on a zoomed-out map (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/5655">#5655</a>, <a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8326">#8326</a>, continues <a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/5956">#5956</a>) (by <a href="https://github.com/yuiseki"><code>@​yuiseki</code></a>)</li>
<li>Fix terrain drape textures not being refreshed after zoom changes, causing stale rendering at the new zoom level (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/8251">#8251</a>) (by <a href="https://github.com/patte"><code>@​patte</code></a>)</li>
<li>Fix a gap between the sky and the ground at high pitch while globe transitions to mercator (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/7382">#7382</a>) (by <a href="https://github.com/birkskyum"><code>@​birkskyum</code></a>)</li>
<li>Treat an empty tile response (e.g. HTTP 204) as no data: raster-DEM tiles now load without elevation instead of failing with a <code>dem dimension mismatch</code> error, and empty raster tiles render as transparent (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/1551">#1551</a>) (by <a href="https://github.com/clement-igonet"><code>@​clement-igonet</code></a>)</li>
<li>Validate the <code>before</code> layer in <code>map.moveLayer</code> before reordering, so passing the id of a layer that does not exist leaves the layer order untouched instead of dropping the moved layer out of it (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/8301">#8301</a>) (by <a href="https://github.com/lazerg"><code>@​lazerg</code></a>)

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
