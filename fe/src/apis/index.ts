import VueInterface from 'vue';
import {PluginObject} from 'vue/types/plugin';
import ApiV2 from '@/apis/api-v2';

class ApiV2Plugin implements PluginObject<any> {
  install(Vue: typeof VueInterface, _?: any): void {
    Vue.prototype.$api2 = new ApiV2();
  }
}

const VueApiV2 = new ApiV2Plugin();
export default VueApiV2;
