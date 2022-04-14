import MockAdapter from 'axios-mock-adapter';
import ReccApiBase, {
  STATUS_CODE_UNAUTHORIZED,
  STATUS_CODE_UNINITIALIZED_SERVICE,
  PATH_TOKEN_REFRESH,
} from '../../src/reccApiBase';
import type {RefreshTokenA} from '../../src/packet/user';
import {UninitializedServiceError, RefreshTokenError} from '../../src/error';
import {AxiosRequestConfig} from 'axios';

describe('reccApiBase', () => {
  let testOrigin: string;
  let api: ReccApiBase;
  let mock: MockAdapter;
  let onRefreshTokenError: number;
  let onRenewalAccessToken: number;
  let onUninitializedService: number;
  let onRegisterRefreshSubscribers: number;
  let onUnregisterRefreshSubscribers: number;
  let renewalAccessToken: string;
  let registerRefreshSubscribers: Array<AxiosRequestConfig>;
  let unregisterRefreshSubscribers: Array<AxiosRequestConfig>;

  beforeEach(() => {
    testOrigin = 'https://localhost:8080';
    api = new ReccApiBase({origin: testOrigin});
    mock = new MockAdapter(api.axios, {delayResponse: 10});

    onRefreshTokenError = 0;
    onRenewalAccessToken = 0;
    onUninitializedService = 0;
    onRegisterRefreshSubscribers = 0;
    onUnregisterRefreshSubscribers = 0;
    renewalAccessToken = '';
    registerRefreshSubscribers = [];
    unregisterRefreshSubscribers = [];
    api.onRefreshTokenError = () => {
      onRefreshTokenError++;
    };
    api.onRenewalAccessToken = (accessToken: string) => {
      onRenewalAccessToken++;
      renewalAccessToken = accessToken;
    };
    api.onUninitializedService = () => {
      onUninitializedService++;
    };
    api.onRegisterRefreshSubscribers = (config: AxiosRequestConfig) => {
      onRegisterRefreshSubscribers++;
      registerRefreshSubscribers.push(config);
    };
    api.onUnregisterRefreshSubscribers = (config: AxiosRequestConfig) => {
      onUnregisterRefreshSubscribers++;
      unregisterRefreshSubscribers.push(config);
    };
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

      await expect(api.get('/')).rejects.toThrowError(UninitializedServiceError);
      expect(mock.history.get[0].url).toEqual('/');
      expect(onRefreshTokenError).toEqual(0);
      expect(onRenewalAccessToken).toEqual(0);
      expect(onUninitializedService).toEqual(1);
      expect(onRegisterRefreshSubscribers).toEqual(0);
      expect(onUnregisterRefreshSubscribers).toEqual(0);
    });

    describe('Refresh Token', () => {
      test('Single Request', async () => {
        const rootUri = `${api.base}/`;
        const tokenRefreshUri = `${api.base}${PATH_TOKEN_REFRESH}`;
        const nextAccessToken = '12345';
        mock.onGet(rootUri).replyOnce(STATUS_CODE_UNAUTHORIZED);
        mock.onPost(tokenRefreshUri).replyOnce(200, {
          access: nextAccessToken,
        } as RefreshTokenA);
        mock.onGet(rootUri).reply(200);

        expect(renewalAccessToken).toBeFalsy();
        expect(api.accessToken).toBeFalsy();

        await api.get('/');
        expect(mock.history.get.length).toEqual(2);
        expect(mock.history.post.length).toEqual(1);
        expect(mock.history.get[0].url).toEqual('/');
        expect(mock.history.get[1].url).toEqual('/');
        expect(mock.history.post[0].url).toEqual(PATH_TOKEN_REFRESH);

        expect(onRefreshTokenError).toEqual(0);
        expect(onRenewalAccessToken).toEqual(1);
        expect(onUninitializedService).toEqual(0);
        expect(onRegisterRefreshSubscribers).toEqual(0);
        expect(onUnregisterRefreshSubscribers).toEqual(0);

        expect(renewalAccessToken).toBeTruthy();
        expect(api.accessToken).toBeTruthy();
        expect(renewalAccessToken).toStrictEqual(api.accessToken);
      });

      test('Multiple Request', async () => {
        const rootUri = `${api.base}/`;
        const tokenRefreshUri = `${api.base}${PATH_TOKEN_REFRESH}`;
        const nextAccessToken = '12345';
        mock.onGet(rootUri).replyOnce(STATUS_CODE_UNAUTHORIZED);
        mock.onGet(rootUri).replyOnce(STATUS_CODE_UNAUTHORIZED);
        mock.onPost(tokenRefreshUri).replyOnce(200, {
          access: nextAccessToken,
        } as RefreshTokenA);
        mock.onGet(rootUri).reply(200);

        expect(renewalAccessToken).toBeFalsy();
        expect(api.accessToken).toBeFalsy();

        await Promise.all([api.get('/'), api.get('/')]);
        // GET: direct=2(fail), interceptor=2(success)
        expect(mock.history.get.length).toEqual(4);
        expect(mock.history.post.length).toEqual(1);
        expect(mock.history.get[0].url).toEqual('/');
        expect(mock.history.get[1].url).toEqual('/');
        expect(mock.history.get[2].url).toEqual('/');
        expect(mock.history.post[0].url).toEqual(PATH_TOKEN_REFRESH);

        expect(onRefreshTokenError).toEqual(0);
        expect(onRenewalAccessToken).toEqual(1);
        expect(onUninitializedService).toEqual(0);
        expect(onRegisterRefreshSubscribers).toEqual(1);
        expect(onUnregisterRefreshSubscribers).toEqual(1);

        expect(registerRefreshSubscribers.length).toEqual(1);
        expect(unregisterRefreshSubscribers.length).toEqual(1);
        expect(registerRefreshSubscribers[0]).toStrictEqual(
          unregisterRefreshSubscribers[0],
        );
        expect(api.refreshSubscribers.length).toEqual(0);

        expect(renewalAccessToken).toBeTruthy();
        expect(api.accessToken).toBeTruthy();
        expect(renewalAccessToken).toStrictEqual(api.accessToken);
      });
    });

    describe('Refresh Token Error', () => {
      beforeEach(() => {
        const rootUri = `${api.base}/`;
        const tokenRefreshUri = `${api.base}${PATH_TOKEN_REFRESH}`;
        mock.onGet(rootUri).reply(STATUS_CODE_UNAUTHORIZED);
        mock.onPost(tokenRefreshUri).reply(STATUS_CODE_UNAUTHORIZED);
      });

      test('Single Request', async () => {
        await expect(api.get('/')).rejects.toThrowError(RefreshTokenError);
        expect(mock.history.get.length).toEqual(1);
        expect(mock.history.post.length).toEqual(1);
        expect(mock.history.get[0].url).toEqual('/');
        expect(mock.history.post[0].url).toEqual(PATH_TOKEN_REFRESH);

        expect(onRefreshTokenError).toEqual(1);
        expect(onRenewalAccessToken).toEqual(0);
        expect(onUninitializedService).toEqual(0);
        expect(onRegisterRefreshSubscribers).toEqual(0);
        expect(onUnregisterRefreshSubscribers).toEqual(0);
      });

      test('Multiple Request', async () => {
        const a = api.get('/');
        const b = api.get('/');
        await expect(Promise.all([a, b])).rejects.toThrowError(RefreshTokenError);

        expect(mock.history.get.length).toEqual(2);
        expect(mock.history.post.length).toEqual(1);
        expect(mock.history.get[0].url).toEqual('/');
        expect(mock.history.get[1].url).toEqual('/');
        expect(mock.history.post[0].url).toEqual(PATH_TOKEN_REFRESH);

        expect(onRefreshTokenError).toEqual(1); // Important !!
        expect(onRenewalAccessToken).toEqual(0);
        expect(onUninitializedService).toEqual(0);
        expect(onRegisterRefreshSubscribers).toEqual(1);
        expect(onUnregisterRefreshSubscribers).toEqual(1);

        expect(registerRefreshSubscribers.length).toEqual(1);
        expect(unregisterRefreshSubscribers.length).toEqual(1);
        expect(registerRefreshSubscribers[0]).toStrictEqual(
          unregisterRefreshSubscribers[0],
        );
        expect(api.refreshSubscribers.length).toEqual(0);
      });
    });
  });
});
