import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import dayjs from 'dayjs';
import { ACTIVITY_PERIODS, filterDevicesAndPositions } from './deviceActivity';

export default (
  keyword,
  filter,
  filterSort,
  filterMap,
  filterActivity,
  positions,
  setFilteredDevices,
  setFilteredPositions,
) => {
  const groups = useSelector((state) => state.groups.items);
  const devices = useSelector((state) => state.devices.items);

  const [nowTick, setNowTick] = useState(() => Date.now());

  useEffect(() => {
    const interval = setInterval(() => setNowTick(Date.now()), 60000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Use a fresh timestamp at calculation time: a device that just reported
    // must never be hidden as "future" against a stale 60s tick. The timer
    // above only triggers re-runs so devices age out of the window.
    const now = Date.now();
    const { devices: filtered, positions: filteredPositions } = filterDevicesAndPositions({
      devices,
      groups,
      positions,
      keyword,
      filter,
      activityPeriod: ACTIVITY_PERIODS[filterActivity] || 0,
      now,
      filterMap,
    });
    switch (filterSort) {
      case 'name':
        filtered.sort((device1, device2) => device1.name.localeCompare(device2.name));
        break;
      case 'lastUpdate':
        filtered.sort((device1, device2) => {
          const time1 = device1.lastUpdate ? dayjs(device1.lastUpdate).valueOf() : 0;
          const time2 = device2.lastUpdate ? dayjs(device2.lastUpdate).valueOf() : 0;
          return time2 - time1;
        });
        break;
      default:
        break;
    }
    setFilteredDevices(filtered);
    setFilteredPositions(filteredPositions);
  }, [
    keyword,
    filter,
    filterSort,
    filterMap,
    filterActivity,
    nowTick,
    groups,
    devices,
    positions,
    setFilteredDevices,
    setFilteredPositions,
  ]);
};
