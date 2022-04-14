import {ReccApiBase} from '../../reccApiBase';
import type {ConfigA, UpdateConfigValueQ} from '../../packet/config';

export class ReccApiDevConfigs extends ReccApiBase {
  getDevConfigs() {
    return this.get<Array<ConfigA>>('/dev/configs');
  }

  getDevConfigsPkey(key: string) {
    return this.get<ConfigA>(`/dev/configs/${key}`);
  }

  patchDevConfigsPkey(key: string, body: UpdateConfigValueQ) {
    return this.patch(`/dev/configs/${key}`, body);
  }
}
