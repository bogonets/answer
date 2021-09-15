export const CATEGORY_PM10 = 'pm10';
export const CATEGORY_PM2_5 = 'pm2.5';
export const CATEGORY_CO2 = 'co2';
export const CATEGORY_HUMIDITY = 'humidity';
export const CATEGORY_TEMPERATURE = 'temperature';

export interface AirjoyA {
    group: string;
    project: string;
    name: string;
    description: string;
    online: boolean;

    as_count: number;
    as_last: string;

    // Native
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

export interface AirjoyQ {
    uid: string;

    // Native
    mode?: number;
    power_state?: number;
    fan_control?: number;
    lock?: number;
    filter_reset?: number;
    sleep_mode?: number;
    time_reservation?: number;
}

export interface AirjoyAsA {
    group: string;
    project: string;
    airjoy_uid: string;

    uid: number;
    author?: string;
    description?: string;
    datetime?: string;

    created_at?: string;
    updated_at?: string;
}

export interface CreateAirjoyAsQ {
    group: string;
    project: string;
    uid: string;

    author: string;
    description: string;
    datetime: string;
}

export interface UpdateAirjoyAsQ {
    group: string;
    project: string;
    uid: string;

    author: string;
    description: string;
    datetime: string;
}

export function createEmptyAirjoyA() {
    return {
        group: '',
        project: '',
        name: '',
        description: '',
        online: false,
        as_count: 0,
        as_last: '',
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
    } as AirjoyA;
}

export function createEmptyAirjoyAsA() {
    return {
        group: '',
        project: '',
        airjoy_uid: '',
        uid: 0,
        author: '',
        description: '',
        datetime: '',
        created_at: '',
        updated_at: '',
    } as AirjoyAsA;
}
