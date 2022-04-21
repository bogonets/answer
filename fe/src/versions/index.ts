import VueInterface from 'vue';
import Vuetify from 'vuetify';
import {PluginObject} from 'vue/types/plugin';
import Package from '@/../package.json';

const VUE_VERSION = VueInterface.version;
const VUETIFY_VERSION = Vuetify.version;
const PACKAGE_VERSION = Package.version;

export class Versions {
  readonly vue = VUE_VERSION;
  readonly vuetify = VUETIFY_VERSION;
  readonly answer = PACKAGE_VERSION;
}

class VersionsPlugin implements PluginObject<any> {
  install(Vue: typeof VueInterface, _?: any): void {
    Vue.prototype.$versions = new Versions();
  }
}

const VueVersions = new VersionsPlugin();
export default VueVersions;
