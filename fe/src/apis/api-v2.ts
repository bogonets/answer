import Vue from 'vue';
import ReccApi from '@recc/api/dist';
import {LocalStore} from '@/store/localStore';
import router from '@/router';
import rootNames from '@/router/names/root';
import {RawLocation} from 'vue-router';

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
}
