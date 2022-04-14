import {ReccApiBase} from '@/reccApiBase';
import type {DaemonA, CreateDaemonQ, UpdateDaemonQ} from '@/packet/daemon';

export class ReccApiAdminDaemon extends ReccApiBase {
  getAdminDaemonPlugins() {
    return this.get<Array<string>>('/admin/daemon/plugins');
  }

  getAdminDaemons() {
    return this.get<Array<DaemonA>>('/admin/daemons');
  }

  postAdminDaemons(body: CreateDaemonQ) {
    return this.post('/admin/daemons', body);
  }

  getAdminDaemonsPdaemon(daemon: string) {
    return this.get<DaemonA>(`/admin/daemons/${daemon}`);
  }

  patchAdminDaemonsPdaemon(daemon: string, body: UpdateDaemonQ) {
    return this.patch(`/admin/daemons/${daemon}`, body);
  }

  deleteAdminDaemonsPdaemon(daemon: string) {
    return this.delete(`/admin/daemons/${daemon}`);
  }

  postAdminDaemonsPdaemonStart(daemon: string) {
    return this.post(`/admin/daemons/${daemon}/start`);
  }

  postAdminDaemonsPdaemonStop(daemon: string) {
    return this.post(`/admin/daemons/${daemon}/stop`);
  }
}
