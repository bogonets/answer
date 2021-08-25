import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import devNames from '@/router/names/dev';

@Component
export default class RouterDev extends Router {
    moveToDev() {
        this.moveTo(devNames.dev);
    }

    moveToDevEnvs() {
        this.moveTo(devNames.devEnvs);
    }
}
