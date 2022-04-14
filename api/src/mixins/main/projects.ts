import {ReccApiBase} from '@/reccApiBase';
import type {MemberA, CreateMemberQ, UpdateMemberQ} from '@/packet/member';
import type {
  ProjectA,
  CreateProjectQ,
  UpdateProjectQ,
  ProjectOverviewA,
} from '@/packet/project';

export class ReccApiMainProjects extends ReccApiBase {
  // -------------
  // Main/Projects
  // -------------

  getMainProjects() {
    return this.get<Array<ProjectA>>('/main/projects');
  }

  postMainProjects(body: CreateProjectQ) {
    return this.post('/main/projects', body);
  }

  getMainProjectsPgroupPproject(group: string, project: string) {
    return this.get<ProjectA>(`/main/projects/${group}/${project}`);
  }

  patchMainProjectsPgroupPproject(
    group: string,
    project: string,
    body: UpdateProjectQ,
  ) {
    return this.patch(`/main/projects/${group}/${project}`, body);
  }

  deleteMainProjectsPgroupProject(group: string, project: string) {
    return this.delete(`/main/projects/${group}/${project}`);
  }

  // ---------------------
  // Main/Projects/Members
  // ---------------------

  getMainProjectsPgroupPprojectMembers(group: string, project: string) {
    return this.get<Array<MemberA>>(`/main/projects/${group}/${project}/members`);
  }

  postMainProjectsPgroupPprojectMembers(
    group: string,
    project: string,
    body: CreateMemberQ,
  ) {
    return this.post(`/main/projects/${group}/${project}/members`, body);
  }

  getMainProjectsPgroupPprojectMembersPmember(
    group: string,
    project: string,
    member: string,
  ) {
    return this.get<MemberA>(`/main/projects/${group}/${project}/members/${member}`);
  }

  patchMainProjectsPgroupPprojectMembersPmember(
    group: string,
    project: string,
    member: string,
    body: UpdateMemberQ,
  ) {
    return this.patch(`/main/projects/${group}/${project}/members/${member}`, body);
  }

  deleteMainProjectsPgroupPprojectMembersPmember(
    group: string,
    project: string,
    member: string,
  ) {
    return this.delete(`/main/projects/${group}/${project}/members/${member}`);
  }

  // ----------------------
  // Main/Projects/Overview
  // ----------------------

  getMainProjectsPgroupPprojectOverview(group: string, project: string) {
    const url = `/main/projects/${group}/${project}/overview`;
    return this.get<ProjectOverviewA>(url);
  }
}
