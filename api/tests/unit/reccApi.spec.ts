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

    test('getPublicHeartbeat', async () => {
      const heartbeatPath = '/public/heartbeat';
      const heartbeatUri = `${ReccApi.global.base}${heartbeatPath}`;
      mock.onGet(heartbeatUri).reply(200);
      await expect(ReccApi.global.getPublicHeartbeat()).resolves.toBeUndefined();
      expect(mock.history.get.length).toEqual(1);
      expect(mock.history.get[0].url).toEqual(heartbeatPath);
    });
  });
});
