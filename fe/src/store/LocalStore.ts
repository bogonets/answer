import VueInterface from 'vue';
import { PluginObject } from 'vue/types/plugin';
import { Store, CommitOptions } from 'vuex';
import VuexPersist from 'vuex-persist'
import { User, Extra } from '@/apis/api-v2';

// Modules
import api from '@/store/modules/api';
import appearance from '@/store/modules/appearance';
import session from '@/store/modules/session';
import translation from '@/store/modules/translation';

const DEFAULT_PERSIST_KEY = 'answer.store.local';
const DEFAULT_STRICT = process.env.NODE_ENV !== 'production';

const API_ORIGIN = 'api/origin';
const TRANSLATION_LANG = 'translation/lang';
const APPEARANCE_DARK = 'appearance/dark';
const SESSION_ALREADY = 'session/already';
const SESSION_ACCESS = 'session/access';
const SESSION_REFRESH = 'session/refresh';
const SESSION_USER = 'session/user';
const SESSION_USER_EXTRA = 'session/userExtra';
const SESSION_USER_EXTRA_DARK = 'session/userExtraDark';
const SESSION_USER_EXTRA_LANG = 'session/userExtraLang';

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

    private getter(key: string): any {
        return this.store.getters[key];
    }

    private setter(key: string, val: any): void {
        return this.store.commit(key, val, this.defaultCommitOptions)
    }

    private clear(key: string): void {
        return this.setter(key, undefined);
    }

    get origin(): string {
        return this.getter(API_ORIGIN) as string;
    }

    set origin(val: string) {
        this.setter(API_ORIGIN, val);
    }

    get lang(): string {
        return this.getter(TRANSLATION_LANG) as string;
    }

    set lang(val: string) {
        this.setter(TRANSLATION_LANG, val);
    }

    get dark(): boolean {
        return this.getter(APPEARANCE_DARK) as boolean;
    }

    set dark(val: boolean) {
        this.setter(APPEARANCE_DARK, val);
    }

    get alreadySession(): boolean {
        return this.getter(SESSION_ALREADY) as boolean;
    }

    get access(): string {
        return this.getter(SESSION_ACCESS) as string;
    }

    set access(val: string) {
        this.setter(SESSION_ACCESS, val);
    }

    get refresh(): string {
        return this.getter(SESSION_REFRESH) as string;
    }

    set refresh(val: string) {
        this.setter(SESSION_REFRESH, val);
    }

    get user(): User {
        return this.getter(SESSION_USER) as User;
    }

    set user(val: User) {
        this.setter(SESSION_USER, val);
    }

    get userExtra(): Extra {
        return this.getter(SESSION_USER_EXTRA) as Extra;
    }

    set userExtra(val: Extra) {
        this.setter(SESSION_USER_EXTRA, val);
    }

    get userExtraDark(): boolean {
        return this.getter(SESSION_USER_EXTRA_DARK) as boolean;
    }

    set userExtraDark(val: boolean) {
        this.setter(SESSION_USER_EXTRA_DARK, val);
    }

    get userExtraLang(): string {
        return this.getter(SESSION_USER_EXTRA_LANG) as string;
    }

    set userExtraLang(val: string) {
        this.setter(SESSION_USER_EXTRA_LANG, val);
    }

    clearSession() {
        this.clear(SESSION_ACCESS);
        this.clear(SESSION_REFRESH);
        this.clear(SESSION_USER);
    }
}

class LocalStorePlugin implements PluginObject<any> {
    install(Vue: typeof VueInterface, options?: any): void {
        Vue.prototype.$localStore = new LocalStore(options);
    }
}

const VueLocalStore = new LocalStorePlugin();
export default VueLocalStore;
