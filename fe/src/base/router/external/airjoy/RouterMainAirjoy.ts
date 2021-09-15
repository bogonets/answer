import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import mainAirjoyNames from '@/router/names/external/airjoy/main';

@Component
export default class RouterMainAirjoy extends Router {
    moveToMainAirjoyAs(
        airjoy?: string,
        group?: string,
        project?: string,
    ) {
        const params = {
            airjoy: airjoy || '',
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoyAs, params);
    }

    moveToMainAirjoyChart(
        airjoy?: string,
        category?: string,
        group?: string,
        project?: string,
    ) {
        const params = {
            airjoy: airjoy || '',
            category: category || '',
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoyChart, params);
    }

    moveToMainAirjoyDetails(airjoy: string, group?: string, project?: string) {
        const params = {
            airjoy: airjoy,
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoyDetails, params);
    }

    moveToMainAirjoyDevices(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoyDevices, params);
    }

    moveToMainAirjoyLive(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoyLive, params);
    }

    moveToMainAirjoySettings(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoySettings, params);
    }

    moveToMainAirjoySummary(group?: string, project?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
        };
        this.moveTo(mainAirjoyNames.mainAirjoySummary, params);
    }
}