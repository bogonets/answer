export type PersistEventCallback = (oldValue: any, newValue: any, url: string) => void;

export default class PersistEvent {

    private static _globalListeners = new Map<string, Array<PersistEventCallback>>();

    static on(name: string, callback: PersistEventCallback) {
        if (!PersistEvent._globalListeners[name]) {
            PersistEvent._globalListeners[name] = new Array<PersistEventCallback>();
        }
        PersistEvent._globalListeners[name].push(callback);
    }

    static off(name: string, callback) {
        if (PersistEvent._globalListeners[name].length) {
            PersistEvent._globalListeners[name].splice(PersistEvent._globalListeners[name].indexOf(callback), 1);
        } else {
            PersistEvent._globalListeners[name] = [];
        }
    }

    static emit(event: StorageEvent) {
        if (!event || !event.key) {
            return;
        }

        const callbacks = PersistEvent._globalListeners[event.key];
        if (!callbacks || callbacks.length == 0) {
            return;
        }

        const _value = (data: string | null) => {
            if (data === null) {
                return null;
            }
            try {
                return JSON.parse(data).value;
            } catch (error) {
                return null;
            }
        };

        callbacks.forEach((listener) => {
            listener(_value(event.newValue), _value(event.oldValue), event.url);
        });
    }
}
