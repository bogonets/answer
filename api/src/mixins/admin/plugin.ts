import {ReccApiBase} from '@/reccApiBase';
import type {PluginNameA} from '@/packet/plugin';

export class ReccApiAdminPlugin extends ReccApiBase {
  getAdminPluginNames() {
    return this.get<Array<PluginNameA>>('/admin/plugin/names');
  }
}
