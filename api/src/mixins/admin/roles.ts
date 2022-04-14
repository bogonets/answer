import {ReccApiBase} from '@/reccApiBase';
import type {RoleA, CreateRoleQ, UpdateRoleQ} from '@/packet/role';

export class ReccApiAdminRoles extends ReccApiBase {
  getAdminRoles() {
    return this.get<Array<RoleA>>('/admin/roles');
  }

  postAdminRoles(body: CreateRoleQ) {
    return this.post('/admin/roles', body);
  }

  getAdminRolesProle(role: string) {
    return this.get<RoleA>(`/admin/roles/${role}`);
  }

  patchAdminRolesProle(role: string, body: UpdateRoleQ) {
    return this.patch(`/admin/roles/${role}`, body);
  }

  deleteAdminRolesProle(role: string) {
    return this.delete(`/admin/roles/${role}`);
  }
}
