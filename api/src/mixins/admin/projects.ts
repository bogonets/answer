import {ReccApiBase} from '@/reccApiBase';
import type {ProjectA, CreateProjectQ, UpdateProjectQ} from '@/packet/project';

export class ReccApiAdminProjects extends ReccApiBase {
  getAdminProjects() {
    return this.get<Array<ProjectA>>('/admin/projects');
  }

  postAdminProjects(body: CreateProjectQ) {
    return this.post('/admin/projects', body);
  }

  getAdminProjectsPgroupPproject(group: string, project: string) {
    return this.get<ProjectA>(`/admin/projects/${group}/${project}`);
  }

  patchAdminProjectsPgroupPproject(
    group: string,
    project: string,
    body: UpdateProjectQ,
  ) {
    return this.patch(`/admin/projects/${group}/${project}`, body);
  }

  deleteAdminProjectsPgroupProject(group: string, project: string) {
    return this.delete(`/admin/projects/${group}/${project}`);
  }
}
