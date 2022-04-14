import {ReccApiBase} from '@/reccApiBase';
import type {GroupA, CreateGroupQ, UpdateGroupQ} from '@/packet/group';

export class ReccApiAdminGroups extends ReccApiBase {
  getAdminGroups() {
    return this.get<Array<GroupA>>('/admin/groups');
  }

  postAdminGroups(body: CreateGroupQ) {
    return this.post('/admin/groups', body);
  }

  getAdminGroupsPgroup(group: string) {
    return this.get<GroupA>(`/admin/groups/${group}`);
  }

  patchAdminGroupsPgroup(group: string, body: UpdateGroupQ) {
    return this.patch(`/admin/groups/${group}`, body);
  }

  deleteAdminGroupsGroup(group: string) {
    return this.delete(`/admin/groups/${group}`);
  }
}
