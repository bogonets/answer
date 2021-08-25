import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import groupNames from '@/router/names/group';

@Component
export default class RouterGroup extends Router {
    moveToGroup(group?: string) {
        const params = {group: group || this.$route.params.group};
        this.moveTo(groupNames.group, params);
    }

    moveToGroupMembers(group?: string) {
        const params = {group: group || this.$route.params.group};
        this.moveTo(groupNames.groupMembers, params);
    }

    moveToGroupSettings(group?: string) {
        const params = {group: group || this.$route.params.group};
        this.moveTo(groupNames.groupSettings, params);
    }
}
