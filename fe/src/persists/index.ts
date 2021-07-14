import VueInterface from 'vue';
import { PluginObject } from 'vue/types/plugin';
import PersistRecc from '@/persists/PersistRecc';
import PersistOptions from '@/persists/PersistOptions';


class PersistPlugin implements PluginObject<any> {
    install(Vue: typeof VueInterface, options?: PersistOptions): void {
        Vue.prototype.$persist = new PersistRecc(options);
    }
}

const VuePersist = new PersistPlugin()
export default VuePersist;
