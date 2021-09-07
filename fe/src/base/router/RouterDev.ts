import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import devNames from '@/router/names/dev';
import adminNames from "@/router/names/admin";

@Component
export default class RouterDev extends Router {
    moveToDev() {
        this.moveToDevOverview();
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
}
