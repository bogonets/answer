import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import selfNames from '@/router/names/self';

@Component
export default class RouterSelf extends Router {
  moveToSelf() {
    this.moveToSelfProfile();
  }

  moveToSelfAppearance() {
    this.moveTo(selfNames.selfAppearance);
  }

  moveToSelfPassword() {
    this.moveTo(selfNames.selfPassword);
  }

  moveToSelfProfile() {
    this.moveTo(selfNames.selfProfile);
  }
}
