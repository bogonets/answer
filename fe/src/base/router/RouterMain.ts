import Component, {mixins} from 'vue-class-component';
import RouterMainAirjoy from '@/base/router/external/airjoy/RouterMainAirjoy';
import mainNames from '@/router/names/main';
import {OEM_AIRJOY} from '@/packet/oem';

@Component
export default class RouterMain extends mixins(RouterMainAirjoy) {
    moveToMain(group?: string, project?: string) {
        const oem = this.$localStore.preference.oem;
        switch (oem) {
            case OEM_AIRJOY:
                this.moveToMainAirjoyDevices(group, project);
                break;
            default:
                this.moveToMainDashboard(group, project);
                break;
        }
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

    moveToMainFiles(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainFiles, group, project);
    }

    moveToMainLayouts(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainLayouts, group, project);
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

    moveToMainTasks(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainTasks, group, project);
    }

    moveToMainVisualProgramming(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVisualProgramming, group, project);
    }

    moveToMainVmsDevices(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsDevices, group, project);
    }

    moveToMainVmsDevicesDiscovery(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsDevicesDiscovery, group, project);
    }

    moveToMainVmsDevicesEdit(
        group?: string, project?: string, device?: string, tab?: string,
    ) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
            device: device || this.$route.params.device,
            tab: tab || this.$route.params.tab,
        };
        this.moveTo(mainNames.mainVmsDevicesEdit, params);
    }

    moveToMainVmsDevicesEditEventConfigs(
        group?: string, project?: string, device?: string
    ) {
        this.moveToMainVmsDevicesEdit(group, project, device, "3");
    }

    moveToMainVmsDevicesEditEventConfigsEdit(
        group?: string, project?: string, device?: string, event?: string,
    ) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
            device: device || this.$route.params.device,
            event: event || this.$route.params.event,
        };
        this.moveTo(mainNames.mainVmsDevicesEditEventConfigsEdit, params);
    }

    moveToMainVmsDevicesEditEventConfigsNew(
        group?: string, project?: string, device?: string,
    ) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
            device: device || this.$route.params.device,
        };
        this.moveTo(mainNames.mainVmsDevicesEditEventConfigsNew, params);
    }

    moveToMainVmsDevicesDiscoveryEpr(group?: string, project?: string, epr?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
            epr: epr || this.$route.params.epr,
        };
        this.moveTo(mainNames.mainVmsDevicesDiscoveryEpr, params);
    }

    moveToMainVmsDevicesNew(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsDevicesNew, group, project);
    }

    moveToMainVmsEventsCalendar(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsEventsCalendar, group, project);
    }

    moveToMainVmsEventsList(group?: string, project?: string, date?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
            date: date || this.$route.params.date,
        };
        this.moveTo(mainNames.mainVmsEventsList, params);
    }

    moveToMainVmsLayouts(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsLayouts, group, project);
    }

    moveToMainVmsLayoutsEdit(group?: string, project?: string, layout?: string) {
        const params = {
            group: group || this.$route.params.group,
            project: project || this.$route.params.project,
            layout: layout || this.$route.params.layout,
        };
        this.moveTo(mainNames.mainVmsLayoutsEdit, params);
    }

    moveToMainVmsLayoutsNew(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsLayoutsNew, group, project);
    }

    moveToMainVmsLive(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsLive, group, project);
    }

    moveToMainVmsUserConfigs(group?: string, project?: string) {
        this._moveToMainSubpage(mainNames.mainVmsUserConfigs, group, project);
    }
}
