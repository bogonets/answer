import {ReccApiBase} from '@/reccApiBase';
import type {InfoA} from '@/packet/info';

export class ReccApiMainInfos extends ReccApiBase {
  getMainInfosOem() {
    return this.get<InfoA>('/main/infos/oem');
  }

  getMainUsernames() {
    return this.get<Array<string>>('/main/usernames');
  }
}
