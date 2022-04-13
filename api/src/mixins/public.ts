import {AxiosResponse, AxiosRequestConfig, AxiosBasicCredentials} from 'axios';
import {ReccApiBase} from '@/reccApiBase';
import type {SigninA, SignupQ} from '@/packet/user';

export class ReccApiPublic extends ReccApiBase {
  getPublicHeartbeat() {
    return this.get('/public/heartbeat');
  }

  getPublicVersion() {
    return this.get<string>('/public/version');
  }

  getPublicStateAlready() {
    return this.get<boolean>('/public/state/already');
  }

  postPublicSignup(body: SignupQ) {
    return this.post('/public/signup', body);
  }

  postPublicSignupAdmin(body: SignupQ) {
    return this.post('/public/signup/admin', body);
  }

  postSignin(username: string, password: string, updateDefaultAuth = true) {
    const auth = {
      username: username,
      password: ReccApiBase.encryptPassword(password),
    } as AxiosBasicCredentials;

    const config = {
      auth: auth,
    } as AxiosRequestConfig;

    return this.axios
      .post('/public/signin', undefined, config)
      .then((response: AxiosResponse) => {
        const result = response.data as SigninA;
        const access = result.access;
        const refresh = result.refresh;
        if (updateDefaultAuth) {
          this.setTokens(access, refresh);
        }
        return result;
      });
  }
}
