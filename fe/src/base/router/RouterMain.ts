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
                this.moveToMainAirjoySummary(group, project);
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
}
