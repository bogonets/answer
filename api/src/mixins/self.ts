import {ReccApiBase} from '../reccApiBase';
import type {UserA, UpdateUserQ, UpdatePasswordQ, UserInfoA} from '../packet/user';

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
    return this.get<Array<UserInfoA>>('/self/extra');
  }

  getSelfExtraPkey(key: string) {
    return this.get<UserInfoA>(`/self/extra/${key}`);
  }

  patchSelfExtraPkey(key: string, value: string) {
    return this.patch(`/self/extra/${key}`, value);
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
