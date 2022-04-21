import VueInterface from 'vue';
import {PluginObject} from 'vue/types/plugin';
import {Store, CommitOptions} from 'vuex';
import VuexPersist from 'vuex-persist';

// Modules
import permission from '@/store/modules/permission';
import vms from '@/store/modules/vms';

// Packets
import type {VmsDiscoveredDeviceA} from '@/packet/vms';

const DEFAULT_PERSIST_KEY = 'answer.store.session';
const DEFAULT_STRICT = process.env.NODE_ENV !== 'production';

const PERMISSION_GROUP = 'permission/group';
const PERMISSION_PROJECT = 'permission/project';
const PERMISSION_PERMISSIONS = 'permission/permissions';
const VMS_WSD = 'vms/wsd';

export interface SessionStoreOptions {
  key?: string;
  strict?: boolean;
  silent?: boolean;
}

export class SessionStore {
  private persist: VuexPersist<any>;
  private store: Store<any>;
  private defaultCommitOptions: CommitOptions;

  constructor(options?: SessionStoreOptions) {
    const key = options && options.key ? options.key : DEFAULT_PERSIST_KEY;
    const strict = options && options.strict ? options.strict : DEFAULT_STRICT;

    this.persist = new VuexPersist({
      key: key,
      storage: window.sessionStorage,
    });

    this.store = new Store({
      modules: {
        permission,
        vms,
      },
      strict: strict,
      plugins: [this.persist.plugin],
    });

    this.defaultCommitOptions = {
      root: false,
    } as CommitOptions;
  }

  setDefaultCommitOptions(options: CommitOptions) {
    this.defaultCommitOptions = options;
  }

  private getter(key: string) {
    return this.store.getters[key];
  }

  private setter(key: string, val: any) {
    return this.store.commit(key, val, this.defaultCommitOptions);
  }

  private clear(key: string) {
    return this.setter(key, undefined);
  }

  clearPermissionGroup() {
    this.clear(PERMISSION_GROUP);
  }

  get permissionGroup() {
    return this.getter(PERMISSION_GROUP) as string;
  }

  set permissionGroup(val: string) {
    this.setter(PERMISSION_GROUP, val);
  }

  clearPermissionProject() {
    this.clear(PERMISSION_PROJECT);
  }

  get permissionProject() {
    return this.getter(PERMISSION_PROJECT) as string;
  }

  set permissionProject(val: string) {
    this.setter(PERMISSION_PROJECT, val);
  }

  get permissionPermissions() {
    return this.getter(PERMISSION_PERMISSIONS) as Array<string>;
  }

  set permissionPermissions(val: Array<string>) {
    this.setter(PERMISSION_PERMISSIONS, val);
  }

  // ---
  // VMS
  // ---

  get vmsWds() {
    return this.getter(VMS_WSD) as Array<VmsDiscoveredDeviceA>;
  }

  set vmsWds(val: Array<VmsDiscoveredDeviceA>) {
    this.setter(VMS_WSD, val);
  }
}

class SessionStorePlugin implements PluginObject<any> {
  install(Vue: typeof VueInterface, options?: any): void {
    Vue.prototype.$sessionStore = new SessionStore(options);
  }
}

const VueSessionStore = new SessionStorePlugin();
export default VueSessionStore;
