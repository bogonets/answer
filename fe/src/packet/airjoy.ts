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

    asCount: number;
    asLast: string;

    // Native
    fwVer: number;
    uid: number;
    pm10: number;
    pm2_5: number;
    co2: number;
    humidity: number;
    temperature: number;
    voc: number;
    mode: number;
    powerState: number;
    fanControl: number;
    lock: number;
    filter: number;
    filterLife: number;
    uvLed: number;
    timeReservation: number;
    sleepMode: number;
}

export interface AirjoyQ {
    uid: string;

    // Native
    mode?: number;
    powerState?: number;
    fanControl?: number;
    lock?: number;
    filterReset?: number;
    sleepMode?: number;
    timeReservation?: number;
}

export interface AirjoyAsA {
    group: string;
    project: string;
    airjoyUid: string;

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
        asCount: 0,
        asLast: '',
        fwVer: 0,
        uid: 0,
        pm10: 0,
        pm2_5: 0,
        co2: 0,
        humidity: 0,
        temperature: 0,
        voc: 0,
        mode: 0,
        powerState: 0,
        fanControl: 0,
        lock: 0,
        filter: 0,
        filterLife: 0,
        uvLed: 0,
        timeReservation: 0,
        sleepMode: 0,
    } as AirjoyA;
}
