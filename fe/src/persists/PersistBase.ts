import MemoryStorage from '@/persists/MemoryStorage';
import PersistOptions from '@/persists/PersistOptions';

export interface ListenerData {
    key: string;
    oldValue: any;
    newValue: any;
    storage: Storage;
    url: string;
}

export type Listener = (ListenerData) => void;

export const STORAGE_TYPE_LOCAL = 'local';
export const STORAGE_TYPE_SESSION = 'session';
export const STORAGE_TYPE_MEMORY = 'memory';

export const DEFAULT_STORAGE_TYPE = STORAGE_TYPE_LOCAL;
export const DEFAULT_PREFIX = 'persist.';

export default class PersistBase {

    private readonly _storage: Storage;
    private readonly _prefix: string;
    private _listeners: Map<string, Set<Listener>>;

    constructor(options?: PersistOptions) {
        const type = (options && options.type) ? options.type : DEFAULT_STORAGE_TYPE;
        const prefix = (options && options.prefix) ? options.prefix : DEFAULT_PREFIX;

        if (type == STORAGE_TYPE_LOCAL) {
            this._storage = window.localStorage;
        } else if (type == STORAGE_TYPE_SESSION) {
            this._storage = window.sessionStorage;
        } else if (type == STORAGE_TYPE_MEMORY) {
            this._storage = new MemoryStorage();
        } else {
            throw new Error(`Unknown storage type: ${type}`);
        }

        this._prefix = prefix;
        this._listeners = new Map<string, Set<Listener>>();

        if (type == STORAGE_TYPE_LOCAL || type == STORAGE_TYPE_SESSION) {
            if (window) {
                if (window.addEventListener) {
                    window.addEventListener('storage', this.onStorage, false);
                } else {
                    window['onstorage'] = this.onStorage;
                }
            } else {
                console.warn('The `window` object does not exist.')
            }
        }
    }

    private onStorage(event: StorageEvent) {
        if (!event || !event.key) {
            return;
        }

        if (!event.key.startsWith(this._prefix)) {
            return;
        }

        const localKey = event.key.substr(this._prefix.length);
        const callbacks = this._listeners.get(localKey) as Set<Listener>;
        if (!callbacks || callbacks.size == 0) {
            return;
        }

        const _value = (data: string | null) => {
            if (!data) {
                return null;
            }
            try {
                return JSON.parse(data).value;
            } catch (error) {
                return null;
            }
        };

        callbacks.forEach((listener: Listener) => {
            let data = {} as ListenerData;
            data.key = localKey;
            data.oldValue = _value(event.oldValue);
            data.newValue = _value(event.newValue);
            data.storage = this._storage;
            data.url = event.url;
            listener(data);
        });
    }

    get length(): number {
        return this._storage.length;
    }

    size(): number {
        return this.length;
    }

    addListener(key: string, listener: Listener): void {
        if (!this._listeners.has(key)) {
            this._listeners.set(key, new Set<Listener>());
        }
        const callbacks = this._listeners.get(key) as Set<Listener>;
        callbacks.add(listener);
    }

    removeListener(key: string, listener: Listener): void {
        if (!this._listeners.has(key)) {
            return;
        }
        const callbacks = this._listeners.get(key) as Set<Listener>;
        callbacks.delete(listener);
    }

    set(key: string, value: any): void {
        const stringifyValue = JSON.stringify({
            value: value,
            datetime: new Date().getTime(),
        });
        this._storage.setItem(this._prefix + key, stringifyValue);
    }

    get(key: string, defaultValue: any = undefined): any {
        const value = this._storage.getItem(this._prefix + key);
        if (value === null) {
            return defaultValue;
        }

        try {
            const data = JSON.parse(value);
            return data.value;
        } catch (error) {
            return defaultValue;
        }
    }

    remove(key: string): void {
        this._storage.removeItem(this._prefix + key);
    }

    clear(): void {
        if (!this.length) {
            return;
        }
        for (const key of this.keys(true)) {
            this._storage.removeItem(key);
        }
    }

    keys(original = false): Array<string> {
        let result = new Array<string>();
        for (let i = 0; i < this.length; i++) {
            const key = this._storage.key(i);
            if (key !== null && key.startsWith(this._prefix)) {
                if (original) {
                    result.push(key);
                } else {
                    result.push(key.substr(this._prefix.length));
                }
            }
        }
        return result;
    }

    has(key: string): boolean {
        const realKey = this._prefix + key;
        for (let i = 0; i < this.length; i++) {
            if (realKey == this._storage.key(i)) {
                return true;
            }
        }
        return false;
    }
}
