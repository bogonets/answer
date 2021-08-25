import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import devNames from '@/router/names/dev';

@Component
export default class RouterDev extends Router {
    moveToDev() {
        this.moveToDevOverview();
    }

    moveToDevEnvs() {
        this.moveTo(devNames.devEnvs);
    }

    moveToDevOverview() {
        this.moveTo(devNames.devOverview);
    }
}
