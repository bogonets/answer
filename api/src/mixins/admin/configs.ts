import {ReccApiBase} from '@/reccApiBase';
import type {ConfigA, UpdateConfigValueQ} from '@/packet/config';

export class ReccApiAdminConfigs extends ReccApiBase {
  getAdminConfigs() {
    return this.get<Array<ConfigA>>('/admin/configs');
  }

  getAdminConfigsPkey(key: string) {
    return this.get<ConfigA>(`/admin/configs/${key}`);
  }

  patchAdminConfigsPkey(key: string, body: UpdateConfigValueQ) {
    return this.patch(`/admin/configs/${key}`, body);
  }
}
