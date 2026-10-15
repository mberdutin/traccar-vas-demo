# pull_request 1937: Bump maplibre-gl from 6.2.0 to 6.3.0

Источник: https://github.com/traccar/traccar-web/pull/1937
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: не указана.
Обновлено в GitHub: 2026-08-13T22:36:15Z.
Тематические слова: изменение реализация фильтр merged PR

## Текст обращения

Bumps [maplibre-gl](https://github.com/maplibre/maplibre-gl-js) from 6.2.0 to 6.3.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/maplibre/maplibre-gl-js/releases">maplibre-gl's releases</a>.</em></p>
<blockquote>
<h2>v6.3.0</h2>
<h3>✨ Features and improvements</h3>
<ul>
<li>Make fired/listened map events typed. This means that <code>map.on(&quot;something&quot;, ...)</code> (and <code>once</code>, <code>listens</code>) will now give you an typescript error and better autocomplete. If you relied on firing/listening custom events via the map, this still works via the escape hatches <code>map.fire(&quot;something&quot; as any)</code> -&gt; <code>map.on(&quot;something&quot; as any, ...)</code> (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/8072">#8072</a>) (by <a href="https://github.com/CommanderStorm"><code>@​CommanderStorm</code></a>)</li>
<li>Let a <code>StyleImageInterface</code> give a <code>{renderWithWebGL}</code> callback as its <code>data</code>, an escape hatch for plugin developers and advanced users that renders a style image on the GPU instead of moving its pixels through the CPU. Nothing new is possible that pixels could not already express, but an image that changes often, such as an animated icon, gets more performant (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/7954">#7954</a>) (by <a href="https://github.com/lucaswoj"><code>@​lucaswoj</code></a>)</li>
<li>Use integer vertex attributes for packed line data instead of float conversion (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/7640">#7640</a>) (by <a href="https://github.com/johncarmack1984"><code>@​johncarmack1984</code></a>)</li>
<li>Use integer vertex attributes for packed circle, heatmap, symbol, and fill-extrusion data instead of float conversion (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/7640">#7640</a>, <a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8143">#8143</a>) (by <a href="https://github.com/johncarmack1984"><code>@​johncarmack1984</code></a>)</li>
<li>Redesign benchmarks to use vitest bench capabilities and remove custom build for benchmarks code (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/982">#982</a>) (by <a href="https://github.com/johncarmack1984"><code>@​johncarmack1984</code></a>)</li>
</ul>
<h3>🐞 Bug fixes</h3>
<ul>
<li>Fix terrain pan/zoom gestures losing the grabbed terrain point: gestures are now solved against the elevation of the terrain under the gesture instead of the frozen center elevation, so terrain under the pointer/fingers no longer slips during moving-centroid pinches and drags (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8067">#8067</a>) (by <a href="https://github.com/StrawberryJam22"><code>@​StrawberryJam22</code></a>)</li>
<li>Fix <code>ImageSource</code>, <code>VideoSource</code> and <code>CanvasSource</code> leaking a GPU texture on every image update and on removal, and a resized texture losing its wrap and filter settings (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8094">#8094</a>) (by <a href="https://github.com/mondsichtung"><code>@​mondsichtung</code></a>)</li>
<li>Fix <code>map.queryRenderedFeatures()</code> sometimes causing &quot;Out of bounds&quot; error due to race condition while loading tile data (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/issues/8064">#8064</a>) (by <a href="https://github.com/smvjohansenbouvet"><code>@​smvjohansenbouvet</code></a>)</li>
<li>Fix zooming the globe with the scroll wheel or a two-finger pinch drifting away from the pointer while the globe is small on screen, instead of keeping the location under the pointer as it does when zoomed in (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/8095">#8095</a>) (by <a href="https://github.com/mondsichtung"><code>@​mondsichtung</code></a>)</li>
<li>Fix projective rendering for non-parallelogram image source quads (<a href="https://redirect.github.com/maplibre/maplibre-gl-js/pull/7887">#7887</a>) (by <a href="https://github.com/i4innovationnet"><code>@​i4innovationnet</code></a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/maplibre/maplibre-gl-js/blob/main/CHANGELOG.md">maplibre-gl's changelog</a>.</em></p>
<blockquote>
<h2>6.3.0</h2>
<h3>✨ Features and improvements</h3>
<ul>
<li>Make fired/lis

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
