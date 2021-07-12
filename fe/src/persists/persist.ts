import MemoryStorage from '@/persists/memory-storage';

const STORAGE_TYPE_LOCAL = 'local';
const STORAGE_TYPE_SESSION = 'session';
const STORAGE_TYPE_MEMORY = 'memory';

const DEFAULT_STORAGE_TYPE = STORAGE_TYPE_LOCAL;
const DEFAULT_PREFIX = 'recc.';

interface PersistOptions {
    type?: string;
    prefix?: string;
}

export default class Persist {

    private _storage: Storage;
    private _prefix: string;

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
    }

    get length(): number {
        return this._storage.length;
    }

    setPrefix(prefix: string): void {
        this._prefix = prefix;
    }

    size(): number {
        return this.length;
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
}
