import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import mainNames from "@/router/names/main";

@Component
export default class RouterMain extends Router {
    moveToMain(group?: string, project?: string) {
        this.moveToMainDashboard(group, project);
    }

    moveToMainDashboard(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainNames.mainDashboard, params);
    }

    moveToMainMembers(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainNames.mainMembers, params);
    }

    moveToMainSettings(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainNames.mainSettings, params);
    }

    moveToMainTables(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainNames.mainTables, params);
    }

    moveToMainVms(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainNames.mainVms, params);
    }
}