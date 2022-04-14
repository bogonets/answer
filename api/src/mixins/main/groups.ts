import {ReccApiBase} from '../../reccApiBase';
import type {GroupA, CreateGroupQ, UpdateGroupQ} from '../../packet/group';
import type {MemberA, CreateMemberQ, UpdateMemberQ} from '../../packet/member';
import type {ProjectA} from '../../packet/project';

export class ReccApiMainGroups extends ReccApiBase {
  // -----------
  // Main/Groups
  // -----------

  getMainGroups() {
    return this.get<Array<GroupA>>('/main/groups');
  }

  postMainGroups(body: CreateGroupQ) {
    return this.post('/main/groups', body);
  }

  getMainGroupsPgroup(group: string) {
    return this.get<GroupA>(`/main/groups/${group}`);
  }

  patchMainGroupsPgroup(group: string, body: UpdateGroupQ) {
    return this.patch(`/main/groups/${group}`, body);
  }

  deleteMainGroupsGroup(group: string) {
    return this.delete(`/main/groups/${group}`);
  }

  // -------------------
  // Main/Groups/Members
  // -------------------

  getMainGroupsPgroupMembers(group: string) {
    return this.get<Array<MemberA>>(`/main/groups/${group}/members`);
  }

  postMainGroupsPgroupMembers(group: string, body: CreateMemberQ) {
    return this.post(`/main/groups/${group}/members`, body);
  }

  getMainGroupsPgroupMembersPmember(group: string, member: string) {
    return this.get<MemberA>(`/main/groups/${group}/members/${member}`);
  }

  patchMainGroupsPgroupMembersPmember(
    group: string,
    member: string,
    body: UpdateMemberQ,
  ) {
    return this.patch(`/main/groups/${group}/members/${member}`, body);
  }

  deleteMainGroupsPgroupMembersPmember(group: string, member: string) {
    return this.delete(`/main/groups/${group}/members/${member}`);
  }

  // --------------------
  // Main/Groups/Projects
  // --------------------

  getMainGroupsPgroupProjects(group: string) {
    return this.get<Array<ProjectA>>(`/main/groups/${group}/projects`);
  }
}
