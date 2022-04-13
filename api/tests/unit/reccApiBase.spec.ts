import MockAdapter from 'axios-mock-adapter';
import ReccApiBase, {
  STATUS_CODE_UNAUTHORIZED,
  STATUS_CODE_UNINITIALIZED_SERVICE,
  PATH_TOKEN_REFRESH,
} from '@/reccApiBase';
import type {RefreshTokenA} from '@/packet/user';
import {UninitializedServiceError} from '@/error';

describe('reccApiBase', () => {
  let api!: ReccApiBase;
  let mock!: MockAdapter;
  let testOrigin!: string;

  beforeAll(() => {
    testOrigin = 'https://localhost:8080';
    api = new ReccApiBase({origin: testOrigin});
    mock = new MockAdapter(api.axios);
  });

  afterEach(() => {
    mock.reset();
  });

  describe('ReccApiBase', () => {
    test('encryptPassword', async () => {
      expect(ReccApiBase.encryptPassword('0000')).toEqual(
        '9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0',
      );
    });

    test('URL APIs', async () => {
      expect(api.base).toStrictEqual(`${testOrigin}/api/v2`);
      expect(api.origin).toStrictEqual(testOrigin);
      expect(api.version).toStrictEqual(2);

      api.version = 3;
      expect(api.base).toStrictEqual(`${testOrigin}/api/v3`);
      expect(api.origin).toStrictEqual(testOrigin);
      expect(api.version).toStrictEqual(3);

      const newOrigin = 'https://remote:20000/subpath';
      api.origin = newOrigin;
      expect(api.base).toStrictEqual(`${newOrigin}/api/v3`);
      expect(api.origin).toStrictEqual(newOrigin);
      expect(api.version).toStrictEqual(3);
    });

    test('Uninitialized service', async () => {
      const rootUri = `${api.base}/`;
      mock.onGet(rootUri).reply(STATUS_CODE_UNINITIALIZED_SERVICE);

      let onUninitializedService = false;
      api.onUninitializedService = () => {
        onUninitializedService = true;
      };

      await expect(api.get('/')).rejects.toThrowError(UninitializedServiceError);
      expect(mock.history.get[0].url).toEqual('/');
      expect(onUninitializedService).toBeTruthy();
    });

    test('Refresh Token', async () => {
      const rootUri = `${api.base}/`;
      const tokenRefreshUri = `${api.base}${PATH_TOKEN_REFRESH}`;
      const nextAccessToken = '12345';
      mock.onGet(rootUri).replyOnce(STATUS_CODE_UNAUTHORIZED);
      mock.onPost(tokenRefreshUri).replyOnce(200, {
        access: nextAccessToken,
      } as RefreshTokenA);
      mock.onGet(rootUri).replyOnce(200);

      let onRefreshTokenError = false;
      let onRenewalAccessToken = false;
      let renewalAccessToken = '';
      let onUninitializedService = false;
      api.onRefreshTokenError = () => {
        onRefreshTokenError = true;
      };
      api.onRenewalAccessToken = accessToken => {
        onRenewalAccessToken = true;
        renewalAccessToken = accessToken;
      };
      api.onUninitializedService = () => {
        onUninitializedService = true;
      };

      await api.get('/');
      expect(mock.history.get.length).toEqual(2);
      expect(mock.history.post.length).toEqual(1);
      expect(mock.history.get[0].url).toEqual('/');
      expect(mock.history.get[1].url).toEqual('/');
      expect(mock.history.post[0].url).toEqual(PATH_TOKEN_REFRESH);

      expect(onRefreshTokenError).toBeFalsy();
      expect(onRenewalAccessToken).toBeTruthy();
      expect(onUninitializedService).toBeFalsy();
      expect(renewalAccessToken).toStrictEqual(api.accessToken);
    });
  });
});
