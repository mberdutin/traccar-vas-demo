import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  ACTIVITY_PERIODS,
  ACTIVITY_PERIOD_KEYS,
  parseLastUpdate,
  isDeviceActive,
  filterDevicesAndPositions,
} from '../src/main/deviceActivity.js';

const NOW = Date.UTC(2026, 9, 15, 12, 0, 0); // 2026-10-15T12:00:00Z

const devices = {
  1: {
    id: 1,
    name: 'Alpha',
    uniqueId: 'A1',
    status: 'online',
    lastUpdate: '2026-10-15T11:30:00.000Z',
  },
  2: {
    id: 2,
    name: 'Beta',
    uniqueId: 'B2',
    status: 'offline',
    lastUpdate: '2026-10-15T00:00:00.000Z',
  },
  3: { id: 3, name: 'Gamma', uniqueId: 'G3', status: 'online', lastUpdate: null },
  4: {
    id: 4,
    name: 'Delta',
    uniqueId: 'D4',
    status: 'online',
    lastUpdate: '2026-10-15T13:00:00.000Z',
  },
};

const positions = {
  1: { deviceId: 1, latitude: 1, longitude: 1 },
  2: { deviceId: 2, latitude: 2, longitude: 2 },
  3: { deviceId: 3, latitude: 3, longitude: 3 },
  4: { deviceId: 4, latitude: 4, longitude: 4 },
};

const emptyFilter = { statuses: [], groups: [], geofences: [] };

const deviceIds = (list) => list.map((device) => device.id).sort();
const positionDeviceIds = (list) => list.map((position) => position.deviceId).sort();

test('ACTIVITY_PERIODS exposes 1h, 6h and 24h periods', () => {
  assert.deepEqual(ACTIVITY_PERIOD_KEYS, ['1h', '6h', '24h']);
  assert.equal(ACTIVITY_PERIODS['1h'], 60 * 60 * 1000);
  assert.equal(ACTIVITY_PERIODS['6h'], 6 * 60 * 60 * 1000);
  assert.equal(ACTIVITY_PERIODS['24h'], 24 * 60 * 60 * 1000);
});

test('parseLastUpdate converts valid timestamps to UTC milliseconds', () => {
  assert.equal(parseLastUpdate('2026-10-15T11:30:00.000Z'), Date.UTC(2026, 9, 15, 11, 30, 0));
  assert.equal(parseLastUpdate('2026-10-15T14:00:00+02:00'), Date.UTC(2026, 9, 15, 12, 0, 0));
  assert.equal(parseLastUpdate('2026-10-15T07:00:00-05:00'), Date.UTC(2026, 9, 15, 12, 0, 0));
});

test('parseLastUpdate returns null for missing or invalid values', () => {
  assert.equal(parseLastUpdate(null), null);
  assert.equal(parseLastUpdate(undefined), null);
  assert.equal(parseLastUpdate(''), null);
  assert.equal(parseLastUpdate('not-a-date'), null);
  assert.equal(parseLastUpdate('2026-13-45T99:99:00Z'), null);
});

test('isDeviceActive with no period keeps every device visible', () => {
  assert.equal(isDeviceActive(devices[1], 0, NOW), true);
  assert.equal(isDeviceActive(devices[3], 0, NOW), true);
  assert.equal(isDeviceActive(devices[4], 0, NOW), true);
  assert.equal(isDeviceActive(undefined, 0, NOW), true);
});

test('isDeviceActive includes both boundaries of the closed interval', () => {
  const period = ACTIVITY_PERIODS['1h'];
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T11:00:00.000Z' }, period, NOW),
    true,
    'lower boundary now - period is included',
  );
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T12:00:00.000Z' }, period, NOW),
    true,
    'upper boundary now is included',
  );
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T10:59:59.999Z' }, period, NOW),
    false,
    'just below the lower boundary is hidden',
  );
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T12:00:00.001Z' }, period, NOW),
    false,
    'just above now (future) is hidden',
  );
});

test('isDeviceActive hides null, invalid and future lastUpdate', () => {
  const period = ACTIVITY_PERIODS['6h'];
  assert.equal(isDeviceActive({ lastUpdate: null }, period, NOW), false);
  assert.equal(isDeviceActive({ lastUpdate: undefined }, period, NOW), false);
  assert.equal(isDeviceActive({ lastUpdate: '' }, period, NOW), false);
  assert.equal(isDeviceActive({ lastUpdate: 'garbage' }, period, NOW), false);
  assert.equal(isDeviceActive({ lastUpdate: '2026-10-15T18:00:00.000Z' }, period, NOW), false);
  assert.equal(isDeviceActive({}, period, NOW), false);
});

test('isDeviceActive is timezone independent for explicit offsets', () => {
  const period = ACTIVITY_PERIODS['1h'];
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T14:00:00+02:00' }, period, NOW),
    true,
    '14:00+02:00 equals 12:00Z, the upper boundary',
  );
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T06:00:00-05:00' }, period, NOW),
    true,
    '06:00-05:00 equals 11:00Z, the lower boundary',
  );
  assert.equal(
    isDeviceActive({ lastUpdate: '2026-10-15T05:59:59-05:00' }, period, NOW),
    false,
    'one second before the lower boundary in local time is hidden',
  );
});

test('a fresh report is visible with a fresh now and hidden only against a stale now', () => {
  const realNow = Date.now();
  const lastUpdate = new Date(realNow - 30 * 1000).toISOString();
  // The hook computes Date.now() at filter time, so a report that just arrived
  // is inside the window and never hidden as "future" by a stale 60s tick.
  assert.equal(isDeviceActive({ lastUpdate }, ACTIVITY_PERIODS['1h'], realNow), true);
  // Against a stale tick the same report would look like the future; the timer
  // only triggers re-runs so devices age out of the window.
  assert.equal(isDeviceActive({ lastUpdate }, ACTIVITY_PERIODS['1h'], realNow - 60 * 1000), false);
});

test('filter applies to list and map together regardless of filterMap', () => {
  const result = filterDevicesAndPositions({
    devices,
    groups: {},
    positions,
    keyword: '',
    filter: emptyFilter,
    activityPeriod: ACTIVITY_PERIODS['1h'],
    now: NOW,
    filterMap: false,
  });
  assert.deepEqual(deviceIds(result.devices), [1]);
  assert.deepEqual(positionDeviceIds(result.positions), [1]);
});

test('old filters keep filterMap semantics: with filterMap=false they limit only the list', () => {
  const result = filterDevicesAndPositions({
    devices,
    groups: {},
    positions,
    keyword: '',
    filter: { statuses: ['offline'], groups: [], geofences: [] },
    activityPeriod: ACTIVITY_PERIODS['1h'],
    now: NOW,
    filterMap: false,
  });
  assert.deepEqual(deviceIds(result.devices), [], 'offline device is too old for the list');
  assert.deepEqual(
    positionDeviceIds(result.positions),
    [1],
    'map still shows the fresh online device because old filters do not limit the map',
  );
});

test('old filters keep filterMap semantics: with filterMap=true they limit map and list', () => {
  const result = filterDevicesAndPositions({
    devices,
    groups: {},
    positions,
    keyword: '',
    filter: { statuses: ['offline'], groups: [], geofences: [] },
    activityPeriod: ACTIVITY_PERIODS['1h'],
    now: NOW,
    filterMap: true,
  });
  assert.deepEqual(deviceIds(result.devices), []);
  assert.deepEqual(positionDeviceIds(result.positions), []);
});

test('activity filter works together with status, group, geofence and keyword filters (AND)', () => {
  const grouped = {
    ...devices,
    5: {
      id: 5,
      name: 'Epsilon',
      uniqueId: 'E5',
      status: 'online',
      groupId: 10,
      lastUpdate: '2026-10-15T11:45:00.000Z',
    },
  };
  const groupedPositions = {
    ...positions,
    5: { deviceId: 5, latitude: 5, longitude: 5, geofenceIds: [20] },
  };
  const result = filterDevicesAndPositions({
    devices: grouped,
    groups: { 10: { id: 10, groupId: 0 } },
    positions: groupedPositions,
    keyword: 'eps',
    filter: { statuses: ['online'], groups: [10], geofences: [20] },
    activityPeriod: ACTIVITY_PERIODS['1h'],
    now: NOW,
    filterMap: true,
  });
  assert.deepEqual(deviceIds(result.devices), [5]);
  assert.deepEqual(positionDeviceIds(result.positions), [5]);
});

test('with activity off and filterMap=false behavior matches the previous default', () => {
  const result = filterDevicesAndPositions({
    devices,
    groups: {},
    positions,
    keyword: '',
    filter: emptyFilter,
    activityPeriod: 0,
    now: NOW,
    filterMap: false,
  });
  assert.deepEqual(deviceIds(result.devices), [1, 2, 3, 4]);
  assert.deepEqual(positionDeviceIds(result.positions), [1, 2, 3, 4]);
});

test('with activity off and filterMap=true old filters limit map and list', () => {
  const result = filterDevicesAndPositions({
    devices,
    groups: {},
    positions,
    keyword: '',
    filter: { statuses: ['online'], groups: [], geofences: [] },
    activityPeriod: 0,
    now: NOW,
    filterMap: true,
  });
  assert.deepEqual(deviceIds(result.devices), [1, 3, 4]);
  assert.deepEqual(positionDeviceIds(result.positions), [1, 3, 4]);
});

test('devices without a position never appear on the map', () => {
  const result = filterDevicesAndPositions({
    devices,
    groups: {},
    positions: { 1: positions[1] },
    keyword: '',
    filter: emptyFilter,
    activityPeriod: ACTIVITY_PERIODS['24h'],
    now: NOW,
    filterMap: false,
  });
  assert.deepEqual(deviceIds(result.devices), [1, 2]);
  assert.deepEqual(positionDeviceIds(result.positions), [1]);
});
