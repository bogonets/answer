export const UNKNOWN_AIRJOY_UID = 0;
export const UNKNOWN_ROUTE_PARAMS_DEVICE = '-';

export const CATEGORY_UNKNOWN = '';
export const CATEGORY_PM10 = 'pm10';
export const CATEGORY_PM2_5 = 'pm2_5';
export const CATEGORY_CO2 = 'co2';
export const CATEGORY_HUMIDITY = 'humidity';
export const CATEGORY_TEMPERATURE = 'temperature';
export const CATEGORY_VOC = 'voc';

export const INDEX_UNKNOWN = -1;
export const INDEX_PM10 = 0;
export const INDEX_PM2_5 = 1;
export const INDEX_CO2 = 2;
export const INDEX_HUMIDITY = 3;
export const INDEX_TEMPERATURE = 4;
export const INDEX_VOC = 5;

export const FILTER_STATUS_NORMAL = 0;
export const FILTER_STATUS_RESET = 1;
export const FILTER_STATUS_EXCHANGE = 2;

export const MODE_AUTO = 0;
export const MODE_MANUAL = 1;

export const FAN_CONTROL_NORMAL = 0;
export const FAN_CONTROL_WEAK = 1;
export const FAN_CONTROL_MEDIUM = 2;
export const FAN_CONTROL_HIGH = 3;
export const FAN_CONTROL_AUTO = 4;
export const FAN_CONTROL_SLEEP = 5;

export const UNLOCK = 0;
export const LOCK = 1;

export const AWAKE = 0;
export const SLEEP = 1;

export const POWER_STATE_OFF = 0;
export const POWER_STATE_ON = 1;

export const MINUTES_IN_DAY = 60 * 24;

export const OFFLINE_CONVERSION_TIMEOUT_SECONDS = 30;

export const SECOND_IN_MILLISECONDS = 1000;
export const MINUTE_IN_MILLISECONDS = 60 * SECOND_IN_MILLISECONDS;

export const STREAMING_UNIT = 6 * SECOND_IN_MILLISECONDS;
export const STREAMING_REFRESH_MILLISECONDS = STREAMING_UNIT;
export const STREAMING_DURATION_MILLISECONDS = 10 * STREAMING_UNIT;
export const STREAMING_UPDATE_INTERVAL_MILLISECONDS = STREAMING_UNIT;
export const STREAMING_FRAME_RATE = 30;

export const VALID_PM10_MIN = undefined;
export const VALID_PM10_MAX = 101;

export const VALID_PM2_5_MIN = undefined;
export const VALID_PM2_5_MAX = 51;

export const VALID_CO2_MIN = 200;
export const VALID_CO2_MAX = 2000;

export const VALID_HUMIDITY_MIN = 0;
export const VALID_HUMIDITY_MAX = 95;

export const VALID_TEMPERATURE_MIN = -20;
export const VALID_TEMPERATURE_MAX = 70;

export const CHART_SCALE_Y_MAX_PM10 = undefined;
export const CHART_SCALE_Y_MAX_PM2_5 = undefined;
export const CHART_SCALE_Y_MAX_CO2 = undefined;
export const CHART_SCALE_Y_MAX_HUMIDITY = undefined; // prev: 100
export const CHART_SCALE_Y_MAX_TEMPERATURE = undefined; // prev: 100
export const CHART_SCALE_Y_MAX_VOC = 3;

export const DEFAULT_CHART_COLOR = '#00AAAAFF';

export enum State {
  Good,
  Normal,
  Warning,
  Danger,
}

export const STATE_RANGE_BY_PM10 = [30, 50, 100];
export const STATE_RANGE_BY_PM2_5 = [15, 25, 50];
export const STATE_RANGE_BY_CO2 = [700, 1500, 2000];
export const STATE_RANGE_BY_VOC = [0, 1, 2];

export function getState(value: number, range: Array<number>) {
  if (value <= range[0]) {
    return State.Good;
  } else if (value <= range[1]) {
    return State.Normal;
  } else if (value <= range[2]) {
    return State.Warning;
  } else {
    return State.Danger;
  }
}

export function getStateByPm10(value: number) {
  return getState(value, STATE_RANGE_BY_PM10);
}

export function getStateByPm2_5(value: number) {
  return getState(value, STATE_RANGE_BY_PM2_5);
}

export function getStateByCo2(value: number) {
  return getState(value, STATE_RANGE_BY_CO2);
}

export function getStateByVoc(value: number) {
  return getState(value, STATE_RANGE_BY_VOC);
}

export function calcHumidity(value: number) {
  return value / 10.0;
}

export function calcHumidityText(value: number) {
  return calcHumidity(value).toFixed(1);
}

export function calcTemperature(value: number) {
  const result = (value - 500.0) / 10.0;
  if (result >= 0) {
    return result;
  } else {
    return 0;
  }
}

export function calcFilterLifeMinutes(value: number) {
  return value * 10;
}

export function calcFilterLifeDays(value: number) {
  const minutes = calcFilterLifeMinutes(value);
  return Math.ceil(minutes / MINUTES_IN_DAY);
}

export function validRange(value: number, min?: number, max?: number) {
  if (typeof min !== 'undefined') {
    if (value <= min) {
      return false;
    }
  }
  if (typeof max !== 'undefined') {
    if (value >= max) {
      return false;
    }
  }
  return true;
}

export function validPm10(value: number) {
  return validRange(value, VALID_PM10_MIN, VALID_PM10_MAX);
}

export function validPm2_5(value: number) {
  return validRange(value, VALID_PM2_5_MIN, VALID_PM2_5_MAX);
}

export function validCo2(value: number) {
  return validRange(value, VALID_CO2_MIN, VALID_CO2_MAX);
}

export function validHumidity(value: number) {
  return validRange(value, VALID_HUMIDITY_MIN, VALID_HUMIDITY_MAX);
}

export function validTemperature(value: number) {
  return validRange(value, VALID_TEMPERATURE_MIN, VALID_TEMPERATURE_MAX);
}

export function categoryIndexByName(name: string) {
  if (name === CATEGORY_PM10) {
    return INDEX_PM10;
  } else if (name === CATEGORY_PM2_5) {
    return INDEX_PM2_5;
  } else if (name === CATEGORY_CO2) {
    return INDEX_CO2;
  } else if (name === CATEGORY_HUMIDITY) {
    return INDEX_HUMIDITY;
  } else if (name === CATEGORY_TEMPERATURE) {
    return INDEX_TEMPERATURE;
  } else if (name === CATEGORY_VOC) {
    return INDEX_VOC;
  } else {
    return INDEX_UNKNOWN;
  }
}

export function categoryNameByIndex(index: number) {
  switch (index) {
    case INDEX_PM10:
      return CATEGORY_PM10;
    case INDEX_PM2_5:
      return CATEGORY_PM2_5;
    case INDEX_CO2:
      return CATEGORY_CO2;
    case INDEX_HUMIDITY:
      return CATEGORY_HUMIDITY;
    case INDEX_TEMPERATURE:
      return CATEGORY_TEMPERATURE;
    case INDEX_VOC:
      return CATEGORY_VOC;
    default:
      return CATEGORY_UNKNOWN;
  }
}

export const PRINTABLE_CATEGORY_NAME = {
  ko: {
    pm10: '미세먼지',
    pm2_5: '초미세먼지',
    co2: '이산화탄소',
    humidity: '습도',
    temperature: '온도',
    voc: 'VOC',
  },
  en: {
    pm10: 'PM10',
    pm2_5: 'PM2.5',
    co2: 'CO2',
    humidity: 'Humidity',
    temperature: 'Temperature',
    voc: 'VOC',
  },
};

export function getChartScaleYMax(index: number) {
  switch (index) {
    case INDEX_PM10:
      return CHART_SCALE_Y_MAX_PM10;
    case INDEX_PM2_5:
      return CHART_SCALE_Y_MAX_PM2_5;
    case INDEX_CO2:
      return CHART_SCALE_Y_MAX_CO2;
    case INDEX_HUMIDITY:
      return CHART_SCALE_Y_MAX_HUMIDITY;
    case INDEX_TEMPERATURE:
      return CHART_SCALE_Y_MAX_TEMPERATURE;
    case INDEX_VOC:
      return CHART_SCALE_Y_MAX_VOC;
    default:
      return undefined;
  }
}

export function printableCategoryNameByIndex(index: number, lang: string) {
  switch (index) {
    case INDEX_PM10:
      return PRINTABLE_CATEGORY_NAME[lang][CATEGORY_PM10];
    case INDEX_PM2_5:
      return PRINTABLE_CATEGORY_NAME[lang][CATEGORY_PM2_5];
    case INDEX_CO2:
      return PRINTABLE_CATEGORY_NAME[lang][CATEGORY_CO2];
    case INDEX_HUMIDITY:
      return PRINTABLE_CATEGORY_NAME[lang][CATEGORY_HUMIDITY];
    case INDEX_TEMPERATURE:
      return PRINTABLE_CATEGORY_NAME[lang][CATEGORY_TEMPERATURE];
    case INDEX_VOC:
      return PRINTABLE_CATEGORY_NAME[lang][CATEGORY_VOC];
    default:
      return CATEGORY_UNKNOWN;
  }
}

export function printableCategoryIndexByName(name: string, lang: string) {
  if (name === PRINTABLE_CATEGORY_NAME[lang][CATEGORY_PM10]) {
    return INDEX_PM10;
  } else if (name === PRINTABLE_CATEGORY_NAME[lang][CATEGORY_PM2_5]) {
    return INDEX_PM2_5;
  } else if (name === PRINTABLE_CATEGORY_NAME[lang][CATEGORY_CO2]) {
    return INDEX_CO2;
  } else if (name === PRINTABLE_CATEGORY_NAME[lang][CATEGORY_HUMIDITY]) {
    return INDEX_HUMIDITY;
  } else if (name === PRINTABLE_CATEGORY_NAME[lang][CATEGORY_TEMPERATURE]) {
    return INDEX_TEMPERATURE;
  } else if (name === PRINTABLE_CATEGORY_NAME[lang][CATEGORY_VOC]) {
    return INDEX_VOC;
  } else {
    return INDEX_UNKNOWN;
  }
}

export function printableCategoryNames(lang: string) {
  return [
    printableCategoryNameByIndex(INDEX_PM10, lang),
    printableCategoryNameByIndex(INDEX_PM2_5, lang),
    printableCategoryNameByIndex(INDEX_CO2, lang),
    printableCategoryNameByIndex(INDEX_HUMIDITY, lang),
    printableCategoryNameByIndex(INDEX_TEMPERATURE, lang),
    printableCategoryNameByIndex(INDEX_VOC, lang),
  ];
}

export interface AirjoySensorA {
  name: string;
  time: string;
  uid: number;
  pm10: number;
  pm2_5: number;
  co2: number;
  humidity: number;
  temperature: number;
  voc: number;
}

export interface AirjoyDeviceA {
  name: string;
  description: string;
  chart_color: string;
  online: boolean;

  service_count: number;
  service_last_time?: string;

  time: string;
  fw_ver: number;
  uid: number;
  pm10: number;
  pm2_5: number;
  co2: number;
  humidity: number;
  temperature: number;
  voc: number;
  mode: number;
  power_state: number;
  fan_control: number;
  lock: number;
  filter: number;
  filter_life: number;
  uv_led: number;
  time_reservation: number;
  sleep_mode: number;
}

export interface AirjoyCreateDeviceQ {
  name: string;
  uid: number;
  description: string;
  chart_color: string;
}

export interface AirjoyUpdateDeviceQ {
  name?: string;
  description?: string;
  chart_color?: string;
}

export interface AirjoyControlQ {
  uid: number;
  mode?: number;
  power_state?: number;
  fan_control?: number;
  lock?: number;
  filter_reset?: number;
  sleep_mode?: number;
  time_reservation?: number;
}

export interface AirjoyChartA {
  begin: string;
  end: string;

  avg_pm10: number;
  avg_pm2_5: number;
  avg_co2: number;
  avg_humidity: number;
  avg_temperature: number;
  avg_voc: number;

  min_pm10: number;
  min_pm2_5: number;
  min_co2: number;
  min_humidity: number;
  min_temperature: number;
  min_voc: number;

  max_pm10: number;
  max_pm2_5: number;
  max_co2: number;
  max_humidity: number;
  max_temperature: number;
  max_voc: number;

  n: number;
}

export interface AirjoyServiceA {
  airjoy_uid: number;
  airjoy_name: string;

  service_uid: number;
  time: string;
  author: string;
  description: string;

  created_at: string;
  updated_at: string;
}

export interface AirjoyCreateServiceQ {
  author: string;
  description: string;
  time: string;
}

export interface AirjoyUpdateServiceQ {
  author: string;
  description: string;
  time: string;
}

export function createEmptyAirjoyDeviceA() {
  return {
    name: '',
    description: '',
    chart_color: '',
    online: false,

    service_count: 0,
    service_last_time: '',

    time: '',
    fw_ver: 0,
    uid: 0,
    pm10: 0,
    pm2_5: 0,
    co2: 0,
    humidity: 0,
    temperature: 0,
    voc: 0,
    mode: 0,
    power_state: 0,
    fan_control: 0,
    lock: 0,
    filter: 0,
    filter_life: 0,
    uv_led: 0,
    time_reservation: 0,
    sleep_mode: 0,
  } as AirjoyDeviceA;
}
