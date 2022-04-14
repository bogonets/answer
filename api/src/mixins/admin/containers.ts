import {ReccApiBase} from '@/reccApiBase';
import type {ContainerA, ControlContainersQ} from '@/packet/container';

export class ReccApiAdminContainers extends ReccApiBase {
  getAdminContainers() {
    return this.get<Array<ContainerA>>('/admin/containers');
  }

  patchAdminContainers(body: ControlContainersQ) {
    return this.patch('/admin/containers', body);
  }
}
