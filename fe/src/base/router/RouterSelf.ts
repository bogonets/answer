import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import selfNames from "@/router/names/self";

@Component
export default class RouterSelf extends Router {
    moveToSelf() {
        this.moveToSelfOverview();
    }

    moveToSelfAppearance() {
        this.moveTo(selfNames.selfAppearance);
    }

    moveToSelfOverview() {
        this.moveTo(selfNames.selfOverview);
    }
}
