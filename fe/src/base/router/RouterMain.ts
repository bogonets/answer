import Component, {mixins} from 'vue-class-component';
import Router from '@/base/router/Router';
import mainNames from '@/router/names/main';
import {OEM_AIRJOY} from '@recc/api/dist/packet/oem';

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

  moveToMainPlugin(
    group?: string,
    project?: string,
    plugin?: string,
    menu?: string,
    path?: string,
  ) {
    const params = {
      group: group || this.$route.params.group,
      project: project || this.$route.params.project,
      plugin: plugin || this.$route.params.plugin,
      menu: menu || this.$route.params.menu,
      path: path || this.$route.params.path,
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

  // REMOVE

  moveToMainDatasets(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainDatasets, group, project);
  }

  moveToMainLabel(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainLabel, group, project);
  }

  moveToMainCategory(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainCategory, group, project);
  }

  moveToMainInstructions(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainInstructions, group, project);
  }

  moveToMainMachineLearning(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainMachineLearning, group, project);
  }

  moveToMainStorage(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainStorage, group, project);
  }

  moveToMainHooks(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainHooks, group, project);
  }

  moveToMainToolSettings(group?: string, project?: string) {
    this._moveToMainSubpage(mainNames.mainToolSettings, group, project);
  }
}
