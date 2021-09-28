import VueInterface from 'vue';
import {PluginObject} from 'vue/types/plugin';
import {Store, CommitOptions} from 'vuex';
import VuexPersist from 'vuex-persist'
import {PermissionA} from '@/packet/permission';

// Modules
import permission from '@/store/modules/permission';

const DEFAULT_PERSIST_KEY = 'answer.store.session';
const DEFAULT_STRICT = process.env.NODE_ENV !== 'production';

const PERMISSION_GROUP = 'permission/group';
const PERMISSION_PROJECT = 'permission/project';
const PERMISSION_FEATURES = 'permission/features';
const PERMISSION_EXTRA = 'permission/extra';
const PERMISSION_LAYOUT_READ = 'permission/layoutRead';
const PERMISSION_LAYOUT_WRITE = 'permission/layoutWrite';
const PERMISSION_STORAGE_READ = 'permission/storageRead';
const PERMISSION_STORAGE_WRITE = 'permission/storageWrite';
const PERMISSION_MANAGER_READ = 'permission/managerRead';
const PERMISSION_MANAGER_WRITE = 'permission/managerWrite';
const PERMISSION_GRAPH_READ = 'permission/graphRead';
const PERMISSION_GRAPH_WRITE = 'permission/graphWrite';
const PERMISSION_MEMBER_READ = 'permission/memberRead';
const PERMISSION_MEMBER_WRITE = 'permission/memberWrite';
const PERMISSION_SETTING_READ = 'permission/settingRead';
const PERMISSION_SETTING_WRITE = 'permission/settingWrite';

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
        const key = (options && options.key) ? options.key : DEFAULT_PERSIST_KEY;
        const strict = (options && options.strict) ? options.strict : DEFAULT_STRICT;

        this.persist = new VuexPersist({
            key: key,
            storage: window.sessionStorage,
        });

        this.store = new Store({
            modules: {
                permission,
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
        return this.store.commit(key, val, this.defaultCommitOptions)
    }

    private clear(key: string) {
        return this.setter(key, undefined);
    }

    get group() {
        return this.getter(PERMISSION_GROUP) as string;
    }

    set group(val: string) {
        this.setter(PERMISSION_GROUP, val);
    }

    get project() {
        return this.getter(PERMISSION_PROJECT) as string;
    }

    set project(val: string) {
        this.setter(PERMISSION_PROJECT, val);
    }

    set permission(val: PermissionA) {
        this.setter(PERMISSION_FEATURES, val.features);
        this.setter(PERMISSION_EXTRA, val.extra);
        this.setter(PERMISSION_LAYOUT_READ, val.r_layout);
        this.setter(PERMISSION_LAYOUT_WRITE, val.w_layout);
        this.setter(PERMISSION_STORAGE_READ, val.r_storage);
        this.setter(PERMISSION_STORAGE_WRITE, val.w_storage);
        this.setter(PERMISSION_MANAGER_READ, val.r_manager);
        this.setter(PERMISSION_MANAGER_WRITE, val.w_manager);
        this.setter(PERMISSION_GRAPH_READ, val.r_graph);
        this.setter(PERMISSION_GRAPH_WRITE, val.w_graph);
        this.setter(PERMISSION_MEMBER_READ, val.r_member);
        this.setter(PERMISSION_MEMBER_WRITE, val.w_member);
        this.setter(PERMISSION_SETTING_READ, val.r_setting);
        this.setter(PERMISSION_SETTING_WRITE, val.w_setting);
    }

    get permissionLayoutRead() {
        return this.getter(PERMISSION_LAYOUT_READ) as boolean;
    }

    get permissionLayoutWrite() {
        return this.getter(PERMISSION_LAYOUT_WRITE) as boolean;
    }

    get permissionStorageRead() {
        return this.getter(PERMISSION_STORAGE_READ) as boolean;
    }

    get permissionStorageWrite() {
        return this.getter(PERMISSION_STORAGE_WRITE) as boolean;
    }

    get permissionManagerRead() {
        return this.getter(PERMISSION_MANAGER_READ) as boolean;
    }

    get permissionManagerWrite() {
        return this.getter(PERMISSION_MANAGER_WRITE) as boolean;
    }

    get permissionGraphRead() {
        return this.getter(PERMISSION_GRAPH_READ) as boolean;
    }

    get permissionGraphWrite() {
        return this.getter(PERMISSION_GRAPH_WRITE) as boolean;
    }

    get permissionMemberRead() {
        return this.getter(PERMISSION_MEMBER_READ) as boolean;
    }

    get permissionMemberWrite() {
        return this.getter(PERMISSION_MEMBER_WRITE) as boolean;
    }

    get permissionSettingRead() {
        return this.getter(PERMISSION_SETTING_READ) as boolean;
    }

    get permissionSettingWrite() {
        return this.getter(PERMISSION_SETTING_WRITE) as boolean;
    }
}

class SessionStorePlugin implements PluginObject<any> {
    install(Vue: typeof VueInterface, options?: any): void {
        Vue.prototype.$sessionStore = new SessionStore(options);
    }
}

const VueSessionStore = new SessionStorePlugin();
export default VueSessionStore;