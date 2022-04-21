import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import adminAirjoyNames from '@/router/names/external/airjoy/admin';

@Component
export default class RouterAdminAirjoy extends Router {
  moveToAdminAirjoyDevices() {
    this.moveTo(adminAirjoyNames.adminAirjoyDevices);
  }
}
