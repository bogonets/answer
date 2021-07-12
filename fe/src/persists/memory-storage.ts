export default class MemoryStorage implements Storage {

    private _dict: Map<string, string>;

    constructor() {
        this._dict = new Map<string, string>();
    }

    get length(): number {
        return this._dict.size;
    }

    clear(): void {
        this._dict.clear();
    }

    getItem(key: string): string | null {
        const result = this._dict.get(key);
        if (result === undefined) {
            return null;
        }
        return result;
    }

    key(index: number): string | null {
        if (0 <= index && index < this._dict.size) {
            const keys = this._dict.keys();
            while (true) {
                if (index) {
                    keys.next();
                    --index;
                } else {
                    return keys.next().value;
                }
            }
        } else {
            return null;
        }
    }

    removeItem(key: string): void {
        this._dict.delete(key);
    }

    setItem(key: string, value: string): void {
        this._dict.set(key, value);
    }
}
