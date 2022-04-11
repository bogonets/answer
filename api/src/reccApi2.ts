import {sha256hex} from '@/crypto';

export class ReccApi {
  static encryptPassword(password: string): string {
    return sha256hex(password);
  }
}

export default ReccApi;
