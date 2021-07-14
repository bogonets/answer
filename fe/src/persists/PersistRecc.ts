import PersistBase, { STORAGE_TYPE_LOCAL } from '@/persists/PersistBase';
import PersistOptions from '@/persists/PersistOptions';

export const DEFAULT_STORAGE_TYPE = STORAGE_TYPE_LOCAL;
export const DEFAULT_PREFIX = 'recc.';

const KEY_API_ORIGIN = "api.origin"

export default class PersistRecc extends PersistBase {

    constructor(options?: PersistOptions) {
        let o = {} as PersistOptions;
        o.type = (options && options.type) ? options.type : DEFAULT_STORAGE_TYPE;
        o.prefix = (options && options.prefix) ? options.prefix : DEFAULT_PREFIX;
        super(options);
    }

    get apiOrigin(): string {
        return super.get(KEY_API_ORIGIN, document.location.origin);
    }

    set apiOrigin(val: string) {
        super.set(KEY_API_ORIGIN, val);
    }
}
