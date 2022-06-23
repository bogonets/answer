import VueInterface from 'vue';
import {PluginObject} from 'vue/types/plugin';
import {Store, CommitOptions} from 'vuex';
import VuexPersist from 'vuex-persist';

const DEFAULT_PERSIST_KEY = 'answer.store.session';
const DEFAULT_STRICT = process.env.NODE_ENV !== 'production';

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
        // EMPTY.
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
}

class SessionStorePlugin implements PluginObject<any> {
  install(Vue: typeof VueInterface, options?: any): void {
    Vue.prototype.$sessionStore = new SessionStore(options);
  }
}

const VueSessionStore = new SessionStorePlugin();
export default VueSessionStore;
