import {ReccApiBase} from '@/reccApiBase';
import type {UserA, UpdateUserQ, SignupQ} from '@/packet/user';

export class ReccApiAdminUsers extends ReccApiBase {
  getAdminUsers() {
    return this.get<Array<UserA>>('/admin/users');
  }

  postAdminUsers(body: SignupQ) {
    return this.post('/admin/users', body);
  }

  getAdminUsersPuser(user: string) {
    return this.get<UserA>(`/admin/users/${user}`);
  }

  patchAdminUsersPuser(user: string, body: UpdateUserQ) {
    return this.patch(`/admin/users/${user}`, body);
  }

  deleteAdminUsersPuser(user: string) {
    return this.delete(`/admin/users/${user}`);
  }
}
