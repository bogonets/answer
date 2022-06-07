import Vue from 'vue';

import ReccApi from '@recc/api/dist';
import {LocalStore} from '@/store/localStore';
import router from '@/router';
import rootNames from '@/router/names/root';
import {RawLocation} from 'vue-router';

import type {
  AirjoySensorA,
  AirjoyDeviceA,
  AirjoyCreateDeviceQ,
  AirjoyUpdateDeviceQ,
  AirjoyControlQ,
  AirjoyChartA,
  AirjoyServiceA,
  AirjoyCreateServiceQ,
  AirjoyUpdateServiceQ,
} from '@/packet/airjoy';

function moveTo(name: string) {
  if (router.currentRoute.name === name) {
    return;
  }

  const rawLocation = {
    name: name,
  } as RawLocation;

  router.push(rawLocation).catch((reason: any) => {
    if (reason.name !== 'NavigationDuplicated') {
      throw reason;
    }
  });
}

function clearSession() {
  const localStore = Vue.prototype.$localStore as LocalStore;
  localStore.clearSession();
}

function renewalAccessToken(access: string) {
  const localStore = Vue.prototype.$localStore as LocalStore;
  localStore.access = access;
}

export default class ApiV2 extends ReccApi {
  constructor() {
    super({
      onRefreshTokenError: () => {
        clearSession();
        moveTo(rootNames.signin);
      },
      onRenewalAccessToken: (accessToken: string) => {
        renewalAccessToken(accessToken);
      },
      onUninitializedService: () => {
        clearSession();
        moveTo(rootNames.init);
      },
    });
  }

  // --------------
  // Plugins/Airjoy
  // --------------

  getAirjoyLive(group: string, project: string) {
    const url = `/plugins/airjoy/${group}/${project}/live`;
    return this.get<Array<AirjoySensorA>>(url);
  }

  getAirjoyDevices(group: string, project: string) {
    const url = `/plugins/airjoy/${group}/${project}/devices`;
    return this.get<Array<AirjoyDeviceA>>(url);
  }

  postAirjoyDevices(group: string, project: string, body: AirjoyCreateDeviceQ) {
    const url = `/plugins/airjoy/${group}/${project}/devices`;
    return this.post(url, body);
  }

  getAirjoyDevice(group: string, project: string, device: number | string) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
    return this.get<AirjoyDeviceA>(url);
  }

  patchAirjoyDevice(
    group: string,
    project: string,
    device: number | string,
    body: AirjoyUpdateDeviceQ,
  ) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
    return this.patch(url, body);
  }

  deleteAirjoyDevice(group: string, project: string, device: number | string) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
    return this.delete(url);
  }

  postAirjoyControl(
    group: string,
    project: string,
    device: number | string,
    body: AirjoyControlQ,
  ) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}/control`;
    return this.post(url, body);
  }

  getAirjoyChart(
    group: string,
    project: string,
    device: number | string,
    begin: string,
    end: string,
  ) {
    const queryBegin = encodeURIComponent(begin);
    const queryEnd = encodeURIComponent(end);
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart`;
    const query = `?begin=${queryBegin}&end=${queryEnd}`;
    return this.get<Array<AirjoyChartA>>(url + query);
  }

  getAirjoyChartCsv(
    group: string,
    project: string,
    device: number | string,
    begin: string,
    end: string,
  ) {
    const queryBegin = encodeURIComponent(begin);
    const queryEnd = encodeURIComponent(end);
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart/csv`;
    const query = `?begin=${queryBegin}&end=${queryEnd}`;
    return this.get<string>(url + query);
  }

  getAirjoyServices(group: string, project: string, device?: number | string) {
    if (typeof device === 'undefined') {
      const url = `/plugins/airjoy/${group}/${project}/services`;
      return this.get<Array<AirjoyServiceA>>(url);
    } else {
      const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
      return this.get<Array<AirjoyServiceA>>(url);
    }
  }

  postAirjoyServices(
    group: string,
    project: string,
    device: number | string,
    body: AirjoyCreateServiceQ,
  ) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
    return this.post(url, body);
  }

  patchAirjoyServices(
    group: string,
    project: string,
    device: number | string,
    service: number | string,
    body: AirjoyUpdateServiceQ,
  ) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services/${service}`;
    return this.patch(url, body);
  }

  deleteAirjoyServices(
    group: string,
    project: string,
    device: number | string,
    service: number | string,
  ) {
    const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services/${service}`;
    return this.delete(url);
  }

  getAirjoyMediaDefaultFile(group: string, project: string) {
    const url = `/plugins/airjoy/${group}/${project}/media/default/file`;
    return this.get(url);
  }

  getAirjoyMediaFileName(group: string, project: string, name: string) {
    const url = `/plugins/airjoy/${group}/${project}/media/file/${name}`;
    return this.get(url);
  }

  getAirjoyMediaList(group: string, project: string) {
    const url = `/plugins/airjoy/${group}/${project}/media/list`;
    return this.get(url);
  }
}
