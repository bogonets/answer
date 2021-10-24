import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import devNames from '@/router/names/dev';

@Component
export default class RouterDev extends Router {
    moveToDev() {
        this.moveToDevOverview();
    }

    moveToDevConfigs() {
        this.moveTo(devNames.devConfigs);
    }

    moveToDevDaemons() {
        this.moveTo(devNames.devDaemons);
    }

    moveToDevEnvs() {
        this.moveTo(devNames.devEnvs);
    }

    moveToDevInfos() {
        this.moveTo(devNames.devInfos);
    }

    moveToDevOverview() {
        this.moveTo(devNames.devOverview);
    }

    moveToDevPlugins() {
        this.moveTo(devNames.devPlugins);
    }
}
