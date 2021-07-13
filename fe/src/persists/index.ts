import VueInterface from 'vue';
import { PluginObject } from 'vue/types/plugin';
import PersistBase from '@/persists/persist-base';

const DEFAULT_PROPERTY_NAME = '$persist';


class PersistPlugin implements PluginObject<any> {
    install(Vue: typeof VueInterface, options: any): void {
        Vue[DEFAULT_PROPERTY_NAME] = new PersistBase(options);
    }
}

const VuePersist = new PersistPlugin()
export default VuePersist;
