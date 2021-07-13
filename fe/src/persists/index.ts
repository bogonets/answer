import VueInterface from 'vue';
import { PluginObject } from 'vue/types/plugin';
import PersistBase from '@/persists/PersistBase';
import PersistOptions from '@/persists/PersistOptions';

const DEFAULT_PROPERTY_NAME = '$persist';


class PersistPlugin implements PluginObject<any> {
    install(Vue: typeof VueInterface, options?: PersistOptions): void {
        Vue[DEFAULT_PROPERTY_NAME] = new PersistBase(options);
    }
}

const VuePersist = new PersistPlugin()
export default VuePersist;
