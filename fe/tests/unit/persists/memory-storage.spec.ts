import MemoryStorage from '@/persists/memory-storage';


describe('MemoryStorage', () => {
    let storage = new MemoryStorage();

    test('default', () => {
        const key0 = 'key0';
        const val0 = 'val0';

        const key1 = 'key1';
        const val1 = 'val1';

        expect(storage.length).toEqual(0);

        storage.setItem(key0, val0);
        expect(storage.length).toEqual(1);
        expect(storage.getItem(key0)).toEqual(val0);
        expect(storage.key(0)).toEqual(key0)

        storage.removeItem(key0);
        expect(storage.length).toEqual(0);

        storage.setItem(key1, val1);
        expect(storage.length).toEqual(1);

        storage.clear();
        expect(storage.length).toEqual(0);
    });

    test('errors', () => {
        const key0 = 'key0';
        const val0 = 'val0';
        const val1 = 'val1';

        storage.setItem(key0, val0);
        storage.setItem(key0, val1);

        expect(storage.length).toEqual(1);
        expect(storage.getItem(key0)).toEqual(val1);

        storage.removeItem(key0);
        expect(storage.length).toEqual(0);
        storage.removeItem(key0);
        expect(storage.length).toEqual(0);

        expect(storage.getItem(key0)).toBeNull();
        expect(storage.key(0)).toBeNull();
    });
});
