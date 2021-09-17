export const CATEGORY_PM10 = 'pm10';
export const CATEGORY_PM2_5 = 'pm2.5';
export const CATEGORY_CO2 = 'co2';
export const CATEGORY_HUMIDITY = 'humidity';
export const CATEGORY_TEMPERATURE = 'temperature';
export const CATEGORY_VOC = 'voc';

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
    online: boolean;

    as_count: number;
    as_last: string;

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

export interface CreateAirjoyDeviceQ {
    name: string;
    uid: number;
    description: string;
}

export interface UpdateAirjoyDeviceQ {
    name: string;
    description: string;
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

export interface AirjoyChartQ {
    begin: string;
    end: string;
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

export interface CreateAirjoyServiceQ {
    author: string;
    description: string;
    time: string;
}

export interface UpdateAirjoyServiceQ {
    author: string;
    description: string;
    time: string;
}

export function createEmptyAirjoyDeviceA() {
    return {
        name: '',
        description: '',
        online: false,

        as_count: 0,
        as_last: '',

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

export function createEmptyAirjoyServiceA() {
    return {
        airjoy_uid: 0,
        airjoy_name: '',

        service_uid: 0,
        time: '',
        author: '',
        description: '',

        created_at: '',
        updated_at: '',
    } as AirjoyServiceA;
}

export function createDemoAirjoyDevices() {
    const items = [
        createEmptyAirjoyDeviceA(),
        createEmptyAirjoyDeviceA(),
        createEmptyAirjoyDeviceA(),
        createEmptyAirjoyDeviceA(),
        createEmptyAirjoyDeviceA(),
    ] as Array<AirjoyDeviceA>;

    items[0].name = 'name1';
    items[1].name = 'name2';
    items[2].name = 'name3';
    items[3].name = 'name4';
    items[4].name = 'name5';

    items[0].description = 'More description1';
    items[1].description = 'More description2';
    items[2].description = 'More description3';
    items[3].description = 'More description4';
    items[4].description = 'More description5';

    items[0].online = true;
    items[1].online = true;
    items[2].online = false;
    items[3].online = false;
    items[4].online = false;

    items[0].as_count = 0;
    items[1].as_count = 0;
    items[2].as_count = 10;
    items[3].as_count = 20;
    items[4].as_count = 30;

    items[0].as_last = '';
    items[1].as_last = '';
    items[2].as_last = '2020-01-01';
    items[3].as_last = '2020-01-02';
    items[4].as_last = '2021-09-10T21:10';

    items[0].fw_ver = 10;
    items[1].fw_ver = 20;
    items[2].fw_ver = 30;
    items[3].fw_ver = 40;
    items[4].fw_ver = 51;

    items[0].uid = 100;
    items[1].uid = 200;
    items[2].uid = 300;
    items[3].uid = 400;
    items[4].uid = 501;

    items[0].pm10 = 0;
    items[1].pm10 = 10;
    items[2].pm10 = 20;
    items[3].pm10 = 30;
    items[4].pm10 = 40;

    items[0].pm2_5 = 0;
    items[1].pm2_5 = 3;
    items[2].pm2_5 = 3.24;
    items[3].pm2_5 = 30;
    items[4].pm2_5 = 100;

    items[0].co2 = 0;
    items[1].co2 = 20;
    items[2].co2 = 30;
    items[3].co2 = 40;
    items[4].co2 = 100;

    items[0].humidity = 0;
    items[1].humidity = 20;
    items[2].humidity = 30;
    items[3].humidity = 40;
    items[4].humidity = 100;

    items[0].temperature = 0;
    items[1].temperature = 20;
    items[2].temperature = 30;
    items[3].temperature = 40;
    items[4].temperature = 100;

    items[0].voc = 0;
    items[1].voc = 1;
    items[2].voc = 2;
    items[3].voc = 3;
    items[4].voc = 3;

    items[0].mode = 0;
    items[1].mode = 0;
    items[2].mode = 1;
    items[3].mode = 1;
    items[4].mode = 1;

    items[0].mode = 0;
    items[1].mode = 0;
    items[2].mode = 1;
    items[3].mode = 1;
    items[4].mode = 1;

    items[0].power_state = 0;
    items[1].power_state = 0;
    items[2].power_state = 1;
    items[3].power_state = 1;
    items[4].power_state = 1;

    items[0].fan_control = 1;
    items[1].fan_control = 2;
    items[2].fan_control = 3;
    items[3].fan_control = 4;
    items[4].fan_control = 5;

    items[0].lock = 0;
    items[1].lock = 0;
    items[2].lock = 1;
    items[3].lock = 1;
    items[4].lock = 1;

    items[0].filter = 0;
    items[1].filter = 0;
    items[2].filter = 1;
    items[3].filter = 1;
    items[4].filter = 2;

    items[0].filter_life = 0;
    items[1].filter_life = 1;
    items[2].filter_life = 10;
    items[3].filter_life = 20;
    items[4].filter_life = 40;

    items[0].uv_led = 0;
    items[1].uv_led = 0;
    items[2].uv_led = 1;
    items[3].uv_led = 1;
    items[4].uv_led = 1;

    items[0].time_reservation = 0;
    items[1].time_reservation = 1;
    items[2].time_reservation = 2;
    items[3].time_reservation = 3;
    items[4].time_reservation = 4;

    items[0].sleep_mode = 0;
    items[1].sleep_mode = 0;
    items[2].sleep_mode = 1;
    items[3].sleep_mode = 1;
    items[4].sleep_mode = 1;

    return items;
}
