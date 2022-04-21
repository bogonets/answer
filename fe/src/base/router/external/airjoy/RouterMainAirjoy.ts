import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import mainAirjoyNames from '@/router/names/external/airjoy/main';

const UNKNOWN_CATEGORY = '-';
const UNKNOWN_DEVICE = '-';

@Component
export default class RouterMainAirjoy extends Router {
  moveToMainAirjoyChart(
    device?: string,
    category?: string,
    group?: string,
    project?: string,
  ) {
    const params = {
      category: category || UNKNOWN_CATEGORY,
      device: device || UNKNOWN_DEVICE,
      group: group || this.$route.params.group,
      project: project || this.$route.params.project,
    };
    this.moveTo(mainAirjoyNames.mainAirjoyChart, params);
  }

  moveToMainAirjoyDetails(device: string, group?: string, project?: string) {
    const params = {
      device: device || UNKNOWN_DEVICE,
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

  moveToMainAirjoyService(device?: string, group?: string, project?: string) {
    const params = {
      device: device || UNKNOWN_DEVICE,
      group: group || this.$route.params.group,
      project: project || this.$route.params.project,
    };
    this.moveTo(mainAirjoyNames.mainAirjoyService, params);
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
