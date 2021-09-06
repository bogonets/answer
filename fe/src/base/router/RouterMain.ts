import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import mainNames from "@/router/names/main";
import AirJoyGraph from "@/components/external/airjoy/AirJoyGraph.vue";

@Component
export default class RouterMain extends Router {
    moveToMain(group?: string, project?: string) {
        this.moveToMainDashboard(group, project);
    }

    private _moveToMainSubpage(routeName: string, group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(routeName, params);
    }

    moveToMainDashboard(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainDashboard, group, project);
    }

    moveToMainMembers(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainMembers, group, project);
    }

    moveToMainSettings(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainSettings, group, project);
    }

    moveToMainTables(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainTables, group, project);
    }

    moveToMainVms(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVms, group, project);
    }

    // ------
    // Airjoy
    // ------

    moveToMainAirjoySummary(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.airjoySummary, group, project);
    }

    moveToMainAirjoyMonitor(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.airjoyMonitor, group, project);
    }

    moveToMainAirJoyGraph(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.airJoyGraph, group, project);
    }
}
