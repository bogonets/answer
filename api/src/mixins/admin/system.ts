import {ReccApiBase} from '@/reccApiBase';
import type {SystemOverviewA} from '@/packet/system';

export class ReccApiAdminSystem extends ReccApiBase {
  getAdminSystemOverview() {
    return this.get<SystemOverviewA>('/admin/system/overview');
  }
}
