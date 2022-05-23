import {Store} from 'vuex';
import type {CommitOptions, Module} from 'vuex';
import VuexPersist from 'vuex-persist';
import type {AsyncStorage} from 'vuex-persist';

export const DEFAULT_STRICT = process.env.NODE_ENV !== 'production';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type State = object;

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type RootState = object;

export interface ReccStoreOptions {
  key: string;
  storage: Storage | AsyncStorage;

  modules?: Record<string, Module<State, RootState>>;
  strict?: boolean;
}

export class ReccStoreBase {
  persist: VuexPersist<State>;
  store: Store<State>;
  commitOptions: CommitOptions;

  constructor(options?: ReccStoreOptions) {
    this.persist = new VuexPersist({
      key: options.key,
      storage: options.storage,
    });
    this.store = new Store({
      modules: options?.modules,
      strict: options?.strict ?? DEFAULT_STRICT,
      plugins: [this.persist.plugin],
    });
    this.commitOptions = {
      root: false,
    } as CommitOptions;
  }

  get(key: string) {
    return this.store.getters[key];
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  set(key: string, value: any) {
    return this.store.commit(key, value, this.commitOptions);
  }

  clear(key: string) {
    return this.set(key, undefined);
  }
}

export default ReccStoreBase;
