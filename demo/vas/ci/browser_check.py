"""Acceptance against the real frontend plus a separate real Traccar API smoke.

Deterministic fixture cases are explicitly isolated from the integration case.
No production app test hooks; Vite module exports inspect actual MapLibre sources.
"""

import argparse
import base64
from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.error
import urllib.request

from playwright.sync_api import sync_playwright, expect

BASE = "http://127.0.0.1:3000"
NOW = "2026-10-15T12:00:00.000Z"
ARTIFACTS = Path("artifacts")
DEVICES = [
    {
        "id": 1,
        "name": "VAS Fresh",
        "uniqueId": "vas-fresh",
        "status": "online",
        "lastUpdate": "2026-10-15T11:45:00Z",
        "groupId": 1,
        "attributes": {},
    },
    {
        "id": 2,
        "name": "VAS Boundary",
        "uniqueId": "vas-boundary",
        "status": "offline",
        "lastUpdate": "2026-10-15T11:00:00Z",
        "groupId": 2,
        "attributes": {},
    },
    {
        "id": 3,
        "name": "VAS Old",
        "uniqueId": "vas-old",
        "status": "online",
        "lastUpdate": "2026-10-15T09:00:00Z",
        "groupId": 1,
        "attributes": {},
    },
    {
        "id": 4,
        "name": "VAS Missing",
        "uniqueId": "vas-missing",
        "status": "unknown",
        "lastUpdate": None,
        "groupId": 2,
        "attributes": {},
    },
    {
        "id": 5,
        "name": "VAS Future",
        "uniqueId": "vas-future",
        "status": "unknown",
        "lastUpdate": "2026-10-15T12:01:00Z",
        "groupId": 2,
        "attributes": {},
    },
]
# VAS Missing (id 4) deliberately has NO position: it must appear in the
# device list but never create a map marker (issue #2 acceptance criterion).
POSITIONS = [
    dict(
        id=d["id"],
        deviceId=d["id"],
        latitude=55.70 + d["id"] * 0.025,
        longitude=37.50 + d["id"] * 0.035,
        fixTime="2026-10-01T00:00:00Z",
        deviceTime="2026-10-01T00:00:00Z",
        serverTime=NOW,
        attributes={},
        geofenceIds=[1],
        speed=0,
        course=0,
        valid=True,
        accuracy=0,
    )
    for d in DEVICES
    if d["id"] != 4
]
SERVER = {
    "id": 1,
    "version": "6.16.0",
    "registration": False,
    "newServer": False,
    "attributes": {
        "activeMapStyles": "locationIqStreets",
        "mapCluster": False,
        "mapDirection": "none",
        "mapLatitude": 55.78,
        "mapLongitude": 37.60,
        "mapZoom": 10,
    },
}
USER = {
    "id": 1,
    "name": "VAS Dispatcher",
    "email": "dispatcher@example.invalid",
    "administrator": False,
    "readonly": True,
    "deviceReadonly": True,
    "attributes": {},
    "map": "locationIqStreets",
    "latitude": 55.78,
    "longitude": 37.60,
    "zoom": 10,
}


def map_ids(page):
    return page.evaluate("""async () => {
      const {map}=await import('/src/map/core/MapView.jsx');
      const ids=new Set();
      for(const source of Object.values(map.getStyle()?.sources||{})) {
        if(source.type==='geojson' && source.data?.features)
          for(const f of source.data.features) if(f.properties?.deviceId) ids.add(Number(f.properties.deviceId));
      }
      return [...ids].sort();
    }""")


def filter_combobox(page, label):
    """Combobox for a MainToolbar filter select.

    The existing Status/Groups/Geofences/Sort By InputLabels have no labelId
    association to their Select, so their comboboxes expose no accessible name
    (only the Activity control does). Select them structurally through the
    FormControl that owns the matching InputLabel instead.
    """
    return page.locator(
        ".MuiFormControl-root",
        has=page.get_by_text(label, exact=True),
    ).get_by_role("combobox")


def reset_badge_case(browser, width):
    """Issue #2: hidden-devices counter and Show all reset above the list."""
    context = browser.new_context(
        viewport={"width": width, "height": 900}, locale="en-US", timezone_id="UTC"
    )
    page = context.new_page()
    page.clock.install(time=datetime.fromisoformat(NOW.replace("Z", "+00:00")))
    page.clock.set_fixed_time(datetime.fromisoformat(NOW.replace("Z", "+00:00")))
    context.add_init_script(
        "localStorage.setItem('language', JSON.stringify('en')); localStorage.setItem('selectedMapStyle',JSON.stringify('locationIqStreets'));"
    )

    def websocket(ws):
        ws.send(json.dumps({"devices": DEVICES, "positions": POSITIONS}))

    page.route_web_socket("**/api/socket", websocket)

    def api(route):
        key = route.request.url.split("/api/", 1)[1].split("?", 1)[0]
        value = {
            "server": SERVER,
            "session": USER,
            "devices": DEVICES,
            "positions": POSITIONS,
            "groups": [
                {"id": 1, "name": "North", "groupId": 0, "attributes": {}},
                {"id": 2, "name": "South", "groupId": 0, "attributes": {}},
            ],
            "geofences": [
                {
                    "id": 1,
                    "name": "Moscow",
                    "area": "CIRCLE (55.75 37.6, 10000)",
                    "attributes": {},
                }
            ],
        }.get(key, [])
        route.fulfill(json=value)

    page.route("**/api/**", api)
    page.route(
        "https://tiles.locationiq.com/**",
        lambda r: r.fulfill(
            json={
                "version": 8,
                "glyphs": "https://cdn.traccar.com/map/fonts/{fontstack}/{range}.pbf",
                "sources": {},
                "layers": [
                    {
                        "id": "background",
                        "type": "background",
                        "paint": {"background-color": "#e4eaf0"},
                    }
                ],
            }
        ),
    )
    page.route("https://cdn.traccar.com/map/fonts/**", lambda r: r.fulfill(body=b""))
    page.goto(BASE)
    if width < 900:
        page.get_by_role("button").filter(
            has=page.locator('[data-testid="DnsIcon"]')
        ).click()
    expect(page.get_by_text("VAS Fresh", exact=True)).to_be_visible(timeout=30000)
    list_body = page.get_by_test_id("deviceListBody")
    bar = page.get_by_test_id("hiddenDevicesBar")

    # Nothing is filtered, so no counter is shown above the list rows.
    expect(bar).to_have_count(0)

    if width >= 900:
        # Persist non-default sort and map-filter settings: Show all must keep both.
        page.get_by_role("button").filter(
            has=page.locator('[data-testid="TuneIcon"]')
        ).click()
        filter_combobox(page, "Sort By").click()
        page.get_by_role("option", name="Name", exact=True).click()
        page.keyboard.press("Escape")
        page.get_by_role("button").filter(
            has=page.locator('[data-testid="TuneIcon"]')
        ).click()
        page.get_by_role("checkbox", name="Filter on Map").check()
        page.keyboard.press("Escape")
        # A selected device row must survive the Show all reset.
        list_body.get_by_text("VAS Fresh", exact=True).click()
        expect(list_body.locator(".Mui-selected")).to_have_count(1)

    # Keyword hides every other device; the counter updates in real time.
    page.get_by_placeholder("Search Devices").fill("Boundary")
    expect(bar).to_be_visible()
    expect(bar).to_contain_text("Hidden: 4")
    expect(list_body.get_by_text("VAS Boundary", exact=True)).to_be_visible()
    expect(list_body.get_by_text("VAS Fresh", exact=True)).to_have_count(0)
    # The bar sits above the rows and never covers them or the map.
    bar_box = bar.bounding_box()
    row_box = list_body.get_by_text("VAS Boundary", exact=True).bounding_box()
    assert bar_box["y"] + bar_box["height"] <= row_box["y"] + 1, "Badge overlaps rows"
    if width < 900:
        assert bar_box["x"] >= 0 and bar_box["x"] + bar_box["width"] <= width, (
            "Badge overflows viewport"
        )
    page.screenshot(
        animations="disabled",
        path=str(ARTIFACTS / f"hidden-badge-keyword-{width}.png"),
    )

    # Activity and status filters combine (AND) with the keyword.
    page.get_by_role("button").filter(
        has=page.locator('[data-testid="TuneIcon"]')
    ).click()
    page.get_by_role("combobox", name="Activity", exact=True).click()
    page.get_by_role("option", name="Last hour", exact=True).click()
    page.keyboard.press("Escape")
    expect(bar).to_contain_text("Hidden: 4")
    page.get_by_placeholder("Search Devices").fill("")
    # With the keyword cleared, the activity window hides three stale devices.
    expect(bar).to_contain_text("Hidden: 3")
    page.get_by_role("button").filter(
        has=page.locator('[data-testid="TuneIcon"]')
    ).click()
    filter_combobox(page, "Status").click()
    page.get_by_role("option", name="Offline (1)", exact=True).click()
    page.keyboard.press("Escape")
    page.keyboard.press("Escape")
    expect(bar).to_contain_text("Hidden: 4")

    # Show all clears every filter but keeps sort and map-filter settings.
    page.get_by_role("button", name="Show all", exact=True).click()
    expect(bar).to_have_count(0)
    for name in ("VAS Fresh", "VAS Boundary", "VAS Old", "VAS Missing", "VAS Future"):
        expect(list_body.get_by_text(name, exact=True)).to_be_visible()
    if width >= 900:
        assert page.evaluate("localStorage.getItem('filterSort')") == '"name"'
        assert page.evaluate("localStorage.getItem('filterMap')") == 'true'
        # The selected row survived the reset.
        expect(list_body.locator(".Mui-selected")).to_have_count(1)
    # All five devices are restored to the list, including the one without
    # coordinates; it must never produce a map marker.
    page.wait_for_function(
        "async () => {const {map}=await import('/src/map/core/MapView.jsx');return map.isStyleLoaded()}"
    )
    page.wait_for_timeout(500)
    assert map_ids(page) == [1, 2, 3, 5], map_ids(page)
    page.screenshot(
        animations="disabled",
        path=str(ARTIFACTS / f"hidden-badge-show-all-{width}.png"),
        full_page=True,
    )
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (
        "Horizontal overflow after Show all"
    )
    context.close()
    print(
        f"PASS issue-2 fixture: {width}px, hidden counter, Show all reset, sort/map/selection keep"
    )


def fixture_case(browser, width):
    context = browser.new_context(
        viewport={"width": width, "height": 900}, locale="en-US", timezone_id="UTC"
    )
    page = context.new_page()
    page.clock.install(time=datetime.fromisoformat(NOW.replace("Z", "+00:00")))
    page.clock.set_fixed_time(datetime.fromisoformat(NOW.replace("Z", "+00:00")))
    context.add_init_script(
        "localStorage.setItem('language', JSON.stringify('en')); localStorage.setItem('selectedMapStyle',JSON.stringify('locationIqStreets'));"
    )
    sockets = []

    def websocket(ws):
        sockets.append(ws)
        ws.send(json.dumps({"devices": DEVICES, "positions": POSITIONS}))

    page.route_web_socket("**/api/socket", websocket)

    def api(route):
        key = route.request.url.split("/api/", 1)[1].split("?", 1)[0]
        value = {
            "server": SERVER,
            "session": USER,
            "devices": DEVICES,
            "positions": POSITIONS,
            "groups": [
                {"id": 1, "name": "North", "groupId": 0, "attributes": {}},
                {"id": 2, "name": "South", "groupId": 0, "attributes": {}},
            ],
            "geofences": [
                {
                    "id": 1,
                    "name": "Moscow",
                    "area": "CIRCLE (55.75 37.6, 10000)",
                    "attributes": {},
                }
            ],
        }.get(key, [])
        route.fulfill(json=value)

    page.route("**/api/**", api)
    page.route(
        "https://tiles.locationiq.com/**",
        lambda r: r.fulfill(
            json={
                "version": 8,
                "glyphs": "https://cdn.traccar.com/map/fonts/{fontstack}/{range}.pbf",
                "sources": {},
                "layers": [
                    {
                        "id": "background",
                        "type": "background",
                        "paint": {"background-color": "#e4eaf0"},
                    }
                ],
            }
        ),
    )
    page.route("https://cdn.traccar.com/map/fonts/**", lambda r: r.fulfill(body=b""))
    page.goto(BASE)
    # Device list is initially hidden on mobile; use the existing map/list button.
    if width < 900:
        page.get_by_role("button").filter(
            has=page.locator('[data-testid="DnsIcon"]')
        ).click()
    expect(page.get_by_text("VAS Fresh", exact=True)).to_be_visible(timeout=30000)
    page.wait_for_function(
        "document.querySelector('canvas.maplibregl-canvas') !== null"
    )
    # The new control lives in the existing filter popup.
    page.get_by_role("button").filter(
        has=page.locator('[data-testid="TuneIcon"]')
    ).click()
    select = page.get_by_role("combobox", name="Activity", exact=True)
    expect(select).to_be_visible()
    bounds = select.bounding_box()
    assert bounds["x"] >= 0 and bounds["x"] + bounds["width"] <= width
    page.screenshot(
        animations="disabled", path=str(ARTIFACTS / f"filter-control-{width}.png")
    )
    select.click()
    page.get_by_role("option", name="Last hour", exact=True).click()
    page.keyboard.press("Escape")
    expect(page.get_by_text("VAS Old", exact=True)).to_have_count(0)
    expect(page.get_by_text("VAS Missing", exact=True)).to_have_count(0)
    expect(page.get_by_text("VAS Future", exact=True)).to_have_count(0)
    expect(page.get_by_text("VAS Boundary", exact=True)).to_be_visible()
    page.wait_for_function(
        "async () => {const {map}=await import('/src/map/core/MapView.jsx');return map.isStyleLoaded()}"
    )
    page.wait_for_timeout(500)
    assert map_ids(page) == [1, 2], map_ids(page)
    page.screenshot(
        animations="disabled",
        path=str(ARTIFACTS / f"activity-{width}.png"),
        full_page=True,
    )
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (
        "Horizontal overflow"
    )
    page.reload()
    if width < 900:
        page.get_by_role("button").filter(
            has=page.locator('[data-testid="DnsIcon"]')
        ).click()
    expect(page.get_by_text("VAS Fresh", exact=True)).to_be_visible(timeout=30000)
    expect(page.get_by_text("VAS Old", exact=True)).to_have_count(0)
    # Live message changes visibility through the real Redux/socket pipeline.
    page.clock.set_fixed_time(
        datetime.fromisoformat(NOW.replace("Z", "+00:00")) + timedelta(seconds=30)
    )
    updated = [
        dict(d, lastUpdate="2026-10-15T12:00:15Z") if d["id"] == 3 else d
        for d in DEVICES
    ]
    for ws in sockets[-1:]:
        ws.send(json.dumps({"devices": updated}))
    expect(page.get_by_text("VAS Old", exact=True)).to_be_visible()
    # Aging without incoming messages expires records at the timer boundary.
    page.clock.set_fixed_time(
        datetime.fromisoformat(NOW.replace("Z", "+00:00")) + timedelta(minutes=62)
    )
    page.clock.fast_forward(60 * 1000)
    expect(page.get_by_text("VAS Fresh", exact=True)).to_have_count(0)
    expect(page.get_by_text("VAS Old", exact=True)).to_have_count(0)
    expect(page.get_by_text("VAS Boundary", exact=True)).to_have_count(0)
    page.wait_for_timeout(200)
    assert map_ids(page) == [], map_ids(page)
    page.get_by_role("button").filter(
        has=page.locator('[data-testid="TuneIcon"]')
    ).click()
    page.get_by_role("button", name="Reset", exact=True).click()
    page.keyboard.press("Escape")
    expect(page.get_by_text("VAS Missing", exact=True)).to_be_visible()
    context.close()
    print(
        f"PASS fixture UI: {width}px, boundaries, map/list, persist, reset, live update, clock expiry"
    )


def request(url, method="GET", data=None, auth=None, content_type="application/json"):
    headers = {}
    if auth:
        headers["Authorization"] = "Basic " + base64.b64encode(auth.encode()).decode()
    if data is not None:
        headers["Content-Type"] = content_type
    payload = (
        json.dumps(data).encode()
        if content_type == "application/json" and data is not None
        else data
    )
    with urllib.request.urlopen(
        urllib.request.Request(url, data=payload, headers=headers, method=method),
        timeout=30,
    ) as r:
        raw = r.read()
        return (
            json.loads(raw)
            if raw and r.headers.get("Content-Type", "").startswith("application/json")
            else raw.decode()
        )


def integration_case(browser):
    backend = os.environ.get("TRACCAR_API_URL")
    assert backend, "TRACCAR_API_URL is required: fixture-only success is insufficient"
    # Isolated demo backend only, protected against accidental writes to another server.
    assert backend.startswith(
        ("http://traccar-vas", "http://127.0.0.1:18082", "http://127.0.0.1:8082")
    )
    email = "vas-ci@example.invalid"
    password = "vas-synthetic-demo"
    auth = f"{email}:{password}"
    server = request(backend + "/api/server")
    if server.get("newServer"):
        # Traccar promotes the first registered user itself. Setting administrator
        # before authentication triggers its permission guard during bootstrap.
        request(
            backend + "/api/users",
            "POST",
            {"name": "VAS CI", "email": email, "password": password},
        )
    devices = request(backend + "/api/devices", auth=auth)
    device = next((d for d in devices if d["uniqueId"] == "vas-ci-osmand"), None)
    if device is None:
        device = request(
            backend + "/api/devices",
            "POST",
            {"name": "VAS API Fleet", "uniqueId": "vas-ci-osmand", "attributes": {}},
            auth,
        )
    # A second, restricted dispatcher proves the API does not expand device access.
    viewer_email = "vas-viewer@example.invalid"
    viewer_password = "vas-synthetic-viewer"
    users = request(backend + "/api/users", auth=auth)
    viewer = next((u for u in users if u["email"] == viewer_email), None)
    if viewer is None:
        viewer = request(
            backend + "/api/users",
            "POST",
            {
                "name": "VAS Dispatcher",
                "email": viewer_email,
                "password": viewer_password,
                "readonly": True,
                "deviceReadonly": True,
            },
            auth,
        )
    if not any(d["uniqueId"] == "vas-ci-hidden" for d in devices):
        request(
            backend + "/api/devices",
            "POST",
            {"name": "VAS Hidden Fleet", "uniqueId": "vas-ci-hidden", "attributes": {}},
            auth,
        )
    try:
        request(
            backend + "/api/permissions",
            "POST",
            {"userId": viewer["id"], "deviceId": device["id"]},
            auth,
        )
    except urllib.error.HTTPError as e:
        if e.code not in (400, 409):
            raise
    viewer_devices = request(
        backend + "/api/devices", auth=f"{viewer_email}:{viewer_password}"
    )
    assert [d["uniqueId"] for d in viewer_devices] == ["vas-ci-osmand"], viewer_devices

    protocol = os.environ["TRACCAR_OSMAND_URL"]
    request(
        protocol + "/?id=vas-ci-osmand&lat=55.75&lon=37.62&timestamp=1792065600&speed=0"
    )
    for _ in range(30):
        devices = request(backend + "/api/devices", auth=auth)
        device = next(d for d in devices if d["uniqueId"] == "vas-ci-osmand")
        if device.get("lastUpdate"):
            break
        time.sleep(1)
    assert device.get("lastUpdate"), device
    for _ in range(30):
        positions = request(backend + "/api/positions", auth=auth)
        if any(p["deviceId"] == device["id"] for p in positions):
            break
        time.sleep(1)
    assert any(p["deviceId"] == device["id"] for p in positions)
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    response = context.request.post(
        BASE + "/api/session", form={"email": viewer_email, "password": viewer_password}
    )
    assert response.status == 200, f"Real Traccar login failed: {response.status}"
    page = context.new_page()
    # Real API and websocket forwarded by Vite to the real backend.
    page.goto(BASE)
    expect(page.get_by_text("VAS API Fleet", exact=True)).to_be_visible(timeout=30000)
    page.get_by_role("button").filter(
        has=page.locator('[data-testid="TuneIcon"]')
    ).click()
    page.get_by_role("combobox", name="Activity", exact=True).click()
    page.get_by_role("option", name="Last hour", exact=True).click()
    page.keyboard.press("Escape")
    expect(page.get_by_text("VAS API Fleet", exact=True)).to_be_visible()
    expect(page.get_by_text("VAS Hidden Fleet", exact=True)).to_have_count(0)
    page.wait_for_timeout(250)
    page.keyboard.press("Escape")
    page.wait_for_timeout(250)
    page.screenshot(
        animations="disabled", path=str(ARTIFACTS / "real-api-integration.png")
    )
    # Issue #2: the hidden counter runs on real restricted data and Show all resets it.
    page.get_by_placeholder("Search Devices").fill("zzz-no-match")
    expect(page.get_by_text("VAS API Fleet", exact=True)).to_have_count(0)
    expect(page.get_by_test_id("hiddenDevicesBar")).to_contain_text("Hidden: 1")
    page.get_by_role("button", name="Show all", exact=True).click()
    expect(page.get_by_test_id("hiddenDevicesBar")).to_have_count(0)
    expect(page.get_by_text("VAS API Fleet", exact=True)).to_be_visible()
    page.screenshot(
        animations="disabled", path=str(ARTIFACTS / "real-api-hidden-counter.png")
    )
    (ARTIFACTS / "backend-integration.json").write_text(
        json.dumps(
            {
                "server_version": server["version"],
                "device_id": device["id"],
                "lastUpdate": device["lastUpdate"],
                "position_count": len(positions),
                "restricted_viewer_device_count": len(viewer_devices),
                "fixTime": next(
                    p["fixTime"] for p in positions if p["deviceId"] == device["id"]
                ),
                "status": "PASS",
            },
            indent=2,
        )
        + "\n"
    )
    context.close()
    print(
        "PASS real Traccar API: create/login, OsmAnd packet, device.lastUpdate, positions, frontend filter"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixtures-only",
        action="store_true",
        help="Authoring check only; never completes CI",
    )
    args = parser.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    log = (ARTIFACTS / "vite.log").open("w")
    vite = subprocess.Popen(
        ["npm", "run", "start", "--", "--host", "127.0.0.1"],
        stdout=log,
        stderr=subprocess.STDOUT,
    )
    try:
        for _ in range(90):
            try:
                urllib.request.urlopen(BASE, timeout=1)
                break
            except (OSError, urllib.error.URLError):
                time.sleep(1)
        else:
            raise TimeoutError("Vite not ready")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                executable_path=os.environ.get("CHROMIUM_PATH"),
                args=[
                    "--no-sandbox",
                    "--use-angle=swiftshader",
                    "--enable-unsafe-swiftshader",
                ],
            )
            fixture_case(browser, 1280)
            fixture_case(browser, 390)
            reset_badge_case(browser, 1280)
            reset_badge_case(browser, 390)
            if not args.fixtures_only:
                integration_case(browser)
            browser.close()
    finally:
        vite.terminate()
        vite.wait(timeout=15)
        log.close()


if __name__ == "__main__":
    main()
