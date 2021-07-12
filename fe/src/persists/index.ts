import VueInterface from 'vue';
import { PluginObject } from 'vue/types/plugin';
import Persist from '@/persists/persist';

const DEFAULT_PROPERTY_NAME = '$persist';


class PersistPlugin implements PluginObject<any> {
    install(Vue: typeof VueInterface, options: any): void {
        Vue[DEFAULT_PROPERTY_NAME] = new Persist(options);
    }
}

const VuePersist = new PersistPlugin()
export default VuePersist;
