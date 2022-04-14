import {ReccApiBase} from '../../reccApiBase';
import type {InfoA, CreateInfoQ, UpdateInfoQ} from '../../packet/info';

export class ReccApiDevInfos extends ReccApiBase {
  getDevInfos() {
    return this.get<Array<InfoA>>('/dev/infos');
  }

  postDevInfos(body: CreateInfoQ) {
    return this.post('/dev/infos', body);
  }

  getDevInfosPkey(key: string) {
    return this.get<InfoA>(`/dev/infos/${key}`);
  }

  patchDevInfosPkey(key: string, body: UpdateInfoQ) {
    return this.patch(`/dev/infos/${key}`, body);
  }

  deleteDevInfo(key: string) {
    return this.delete(`/dev/infos/${key}`);
  }
}
