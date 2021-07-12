import Persist from '@/persists/persist';

describe.each(['memory', 'local', 'session'])('Persist', (type) => {
    let storage = new Persist({type: type, prefix: 'test.'});

    test(`${type}-default`, () => {
        const key0 = 'key0';
        const val0 = 'val0';

        const key1 = 'key1';
        const val1 = 'val1';

        expect(storage.length).toEqual(0);

        storage.set(key0, val0);
        expect(storage.length).toEqual(1);
        expect(storage.get(key0)).toEqual(val0);
        expect(storage.keys().length).toEqual(1)
        expect(storage.keys()[0]).toEqual(key0)

        storage.remove(key0);
        expect(storage.length).toEqual(0);

        storage.set(key1, val1);
        expect(storage.length).toEqual(1);

        storage.clear();
        expect(storage.length).toEqual(0);
    });
});
