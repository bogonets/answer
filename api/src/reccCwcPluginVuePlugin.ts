import {ReccCwcPlugin} from './reccCwcPlugin';
import type {ReccCwcPluginOptions} from './reccCwcPlugin';

class ReccCwcPluginVuePlugin {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  install(Vue: any, options?: ReccCwcPluginOptions): void {
    Vue.prototype.$recc = new ReccCwcPlugin(window, options);
  }
}

const VueReccCwcPlugin = new ReccCwcPluginVuePlugin();
export default VueReccCwcPlugin;
