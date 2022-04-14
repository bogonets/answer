import {ReccApiBase} from '@/reccApiBase';
import type {RoleA} from '@/packet/role';

export class ReccApiMainRoles extends ReccApiBase {
  getMainRoles() {
    return this.get<Array<RoleA>>('/main/roles');
  }

  getMainRolesPgroup(group: string) {
    return this.get<RoleA>(`/main/roles/${group}`);
  }

  getMainRolesPgroupPproject(group: string, project: string) {
    return this.get<RoleA>(`/main/roles/${group}/${project}`);
  }
}
