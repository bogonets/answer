import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import groupNames from '@/router/names/group';

@Component
export default class RouterGroup extends Router {
  moveToGroup(group?: string) {
    this.moveToGroupProjects(group);
  }

  moveToGroupMembers(group?: string) {
    const params = {group: group || this.$route.params.group};
    this.moveTo(groupNames.groupMembers, params);
  }

  moveToGroupProjects(group?: string) {
    const params = {group: group || this.$route.params.group};
    this.moveTo(groupNames.groupProjects, params);
  }

  moveToGroupProjectsNew(group?: string) {
    const params = {group: group || this.$route.params.group};
    this.moveTo(groupNames.groupProjectsNew, params);
  }

  moveToGroupSettings(group?: string) {
    const params = {group: group || this.$route.params.group};
    this.moveTo(groupNames.groupSettings, params);
  }
}
