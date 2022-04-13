import {ReccApiBase} from '@/reccApiBase';
import type {UserA, UpdateUserQ, UpdatePasswordQ, UserExtraA} from '@/packet/user';

export class ReccApiSelf extends ReccApiBase {
  getSelf() {
    return this.get<UserA>('/self');
  }

  patchSelf(body: UpdateUserQ) {
    return this.patch<UserA>('/self', body);
  }

  deleteSelf() {
    return this.delete('/self');
  }

  getSelfExtra() {
    return this.get<UserExtraA>('/self/extra');
  }

  patchSelfExtra(extra: UserExtraA) {
    return this.patch('/self/extra', extra);
  }

  patchSelfPassword(body: UpdatePasswordQ) {
    return this.patch('/self/password', body);
  }

  getSelfPermissionsPgroup(group: string) {
    return this.get<Array<string>>(`/self/permissions/${group}`);
  }

  getSelfPermissionsPgroupPproject(group: string, project: string) {
    return this.get<Array<string>>(`/self/permissions/${group}/${project}`);
  }
}
