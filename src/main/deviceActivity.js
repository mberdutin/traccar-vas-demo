export const ACTIVITY_PERIODS = {
  '1h': 60 * 60 * 1000,
  '6h': 6 * 60 * 60 * 1000,
  '24h': 24 * 60 * 60 * 1000,
};

export const ACTIVITY_PERIOD_KEYS = Object.keys(ACTIVITY_PERIODS);

export const parseLastUpdate = (value) => {
  if (value === null || value === undefined || value === '') {
    return null;
  }
  const time = Date.parse(value);
  return Number.isFinite(time) ? time : null;
};

export const isDeviceActive = (device, period, now) => {
  if (!period) {
    return true;
  }
  const lastUpdate = parseLastUpdate(device?.lastUpdate);
  if (lastUpdate === null) {
    return false;
  }
  return lastUpdate >= now - period && lastUpdate <= now;
};

const matchesKeyword = (device, keyword) => {
  const lowerCaseKeyword = keyword.toLowerCase();
  return [device.name, device.uniqueId, device.phone, device.model, device.contact].some(
    (s) => s && s.toLowerCase().includes(lowerCaseKeyword),
  );
};

const deviceGroupIds = (device, groups) => {
  const groupIds = [];
  let { groupId } = device;
  while (groupId) {
    groupIds.push(groupId);
    groupId = groups[groupId]?.groupId || 0;
  }
  return groupIds;
};

export const filterDevicesAndPositions = ({
  devices,
  groups,
  positions,
  keyword,
  filter,
  activityPeriod,
  now,
  filterMap,
}) => {
  const filtered = Object.values(devices)
    .filter((device) => !filter.statuses.length || filter.statuses.includes(device.status))
    .filter(
      (device) =>
        !filter.groups.length ||
        deviceGroupIds(device, groups).some((id) => filter.groups.includes(id)),
    )
    .filter(
      (device) =>
        !filter.geofences.length ||
        (positions[device.id]?.geofenceIds || []).some((id) => filter.geofences.includes(id)),
    )
    .filter((device) => matchesKeyword(device, keyword))
    .filter((device) => isDeviceActive(device, activityPeriod, now));

  const activityDeviceIds = new Set(
    Object.values(devices)
      .filter((device) => isDeviceActive(device, activityPeriod, now))
      .map((device) => device.id),
  );

  const filteredPositions = filterMap
    ? filtered.map((device) => positions[device.id]).filter(Boolean)
    : Object.values(positions).filter((position) => activityDeviceIds.has(position.deviceId));

  return { devices: filtered, positions: filteredPositions };
};
