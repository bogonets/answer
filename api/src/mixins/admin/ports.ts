import {ReccApiBase} from '../../reccApiBase';
import type {PortA, PortRangeA} from '../../packet/port';

export class ReccApiAdminPorts extends ReccApiBase {
  getAdminPortRange() {
    return this.get<PortRangeA>('/admin/port/range');
  }

  getAdminPortNext() {
    return this.get<number>('/admin/port/next');
  }

  getAdminPorts() {
    return this.get<Array<PortA>>('/admin/ports');
  }
}
