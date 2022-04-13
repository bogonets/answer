import MockAdapter from 'axios-mock-adapter';
import ReccApi from '@/reccApi';

describe('reccApi', () => {
  let mock!: MockAdapter;

  beforeAll(() => {
    mock = new MockAdapter(ReccApi.global.axios);
  });

  afterEach(() => {
    mock.reset();
  });

  describe('ReccApi', () => {
    test('Global instance is strict equal', async () => {
      expect(ReccApi.global).toStrictEqual(ReccApi.global);
    });
  });
});
