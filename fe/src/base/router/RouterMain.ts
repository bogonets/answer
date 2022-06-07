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

  moveToMainKanban(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainKanban, group, project);
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

  moveToMainPlugin(plugin: string, menu: string, group?: string, project?: string) {
    const params = {
      plugin: plugin || this.$route.params.plugin,
      menu: menu || this.$route.params.menu,
      group: group || this.$route.params.group,
      project: project || this.$route.params.project,
    };
    this.moveTo(mainNames.mainPlugin, params);
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
}
