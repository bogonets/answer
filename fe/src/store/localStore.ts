import VueInterface from 'vue';
import {PluginObject} from 'vue/types/plugin';
import {Store, CommitOptions} from 'vuex';
import VuexPersist from 'vuex-persist';

// Packets
import type {UserA, UserExtraA} from '@/packet/user';
import type {PreferenceA} from '@/packet/preference';

// Modules
import api from '@/store/modules/api';
import appearance from '@/store/modules/appearance';
import dev from '@/store/modules/dev';
import session from '@/store/modules/session';
import translation from '@/store/modules/translation';

const DEFAULT_PERSIST_KEY = 'answer.store.local';
const DEFAULT_STRICT = process.env.NODE_ENV !== 'production';

const API_ORIGIN = 'api/origin';
const APPEARANCE_DARK = 'appearance/dark';
const APPEARANCE_TIMEZONE = 'appearance/timezone';
const DEV_ENABLE = 'dev/enable';
const SESSION_ALREADY = 'session/already';
const SESSION_ACCESS = 'session/access';
const SESSION_REFRESH = 'session/refresh';
const SESSION_USER = 'session/user';
const SESSION_USER_EXTRA = 'session/userExtra';
const SESSION_USER_EXTRA_DARK = 'session/userExtraDark';
const SESSION_USER_EXTRA_LANG = 'session/userExtraLang';
const SESSION_USER_EXTRA_TIMEZONE = 'session/userExtraTimezone';
const SESSION_PREFERENCE = 'session/preference';
const TRANSLATION_LANG = 'translation/lang';

export interface LocalStoreOptions {
  key?: string;
  strict?: boolean;
  silent?: boolean;
}

export class LocalStore {

  private persist: VuexPersist<any>;
  private store: Store<any>;
  private defaultCommitOptions: CommitOptions;

  constructor(options?: LocalStoreOptions) {
    const key = (options && options.key) ? options.key : DEFAULT_PERSIST_KEY;
    const strict = (options && options.strict) ? options.strict : DEFAULT_STRICT;

    this.persist = new VuexPersist({
      key: key,
      storage: window.localStorage,
    });

    this.store = new Store({
      modules: {
        api,
        appearance,
        dev,
        session,
        translation,
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

  get origin() {
    return this.getter(API_ORIGIN) as string;
  }

  set origin(val: string) {
    this.setter(API_ORIGIN, val);
  }

  get dark() {
    return this.getter(APPEARANCE_DARK) as boolean;
  }

  set dark(val: boolean) {
    this.setter(APPEARANCE_DARK, val);
  }

  get timezone() {
    return this.getter(APPEARANCE_TIMEZONE) as string;
  }

  set timezone(val: string) {
    this.setter(APPEARANCE_TIMEZONE, val);
  }

  get devEnable() {
    return this.getter(DEV_ENABLE) as boolean;
  }

  set devEnable(val: boolean) {
    this.setter(DEV_ENABLE, val);
  }

  get alreadySession() {
    return this.getter(SESSION_ALREADY) as boolean;
  }

  get access() {
    return this.getter(SESSION_ACCESS) as string;
  }

  set access(val: string) {
    this.setter(SESSION_ACCESS, val);
  }

  get refresh() {
    return this.getter(SESSION_REFRESH) as string;
  }

  set refresh(val: string) {
    this.setter(SESSION_REFRESH, val);
  }

  get user() {
    return this.getter(SESSION_USER) as UserA;
  }

  set user(val: UserA) {
    this.setter(SESSION_USER, val);
  }

  get preference() {
    return this.getter(SESSION_PREFERENCE) as PreferenceA;
  }

  set preference(val: PreferenceA) {
    this.setter(SESSION_PREFERENCE, val);
  }

  get userExtra() {
    return this.getter(SESSION_USER_EXTRA) as UserExtraA;
  }

  set userExtra(val: UserExtraA) {
    this.setter(SESSION_USER_EXTRA, val);
  }

  get userExtraDark() {
    return this.getter(SESSION_USER_EXTRA_DARK) as boolean;
  }

  set userExtraDark(val: boolean) {
    this.setter(SESSION_USER_EXTRA_DARK, val);
  }

  get userExtraLang() {
    return this.getter(SESSION_USER_EXTRA_LANG) as string;
  }

  set userExtraLang(val: string) {
    this.setter(SESSION_USER_EXTRA_LANG, val);
  }

  get userExtraTimezone() {
    return this.getter(SESSION_USER_EXTRA_TIMEZONE) as string;
  }

  set userExtraTimezone(val: string) {
    this.setter(SESSION_USER_EXTRA_TIMEZONE, val);
  }

  clearSession() {
    this.clear(SESSION_ACCESS);
    this.clear(SESSION_REFRESH);
    this.clear(SESSION_USER);
  }

  get lang() {
    return this.getter(TRANSLATION_LANG) as string;
  }

  set lang(val: string) {
    this.setter(TRANSLATION_LANG, val);
  }
}

class LocalStorePlugin implements PluginObject<any> {
  install(Vue: typeof VueInterface, options?: any): void {
    Vue.prototype.$localStore = new LocalStore(options);
  }
}

const VueLocalStore = new LocalStorePlugin();
export default VueLocalStore;
