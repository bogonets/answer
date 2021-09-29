import {Component} from 'vue-property-decorator';
import Router from '@/base/router/Router';
import rootNames from "@/router/names/root";

@Component
export default class RouterRoot extends Router {
    moveToInit() {
        this.moveTo(rootNames.init);
    }

    moveToSignup() {
        this.moveTo(rootNames.signup);
    }

    moveToSignin() {
        this.moveTo(rootNames.signin);
    }

    moveToRoot() {
        this.moveTo(rootNames.root);
    }

    moveToRootGroups() {
        this.moveTo(rootNames.rootGroups);
    }

    moveToRootGroupsNew() {
        this.moveTo(rootNames.rootGroupsNew);
    }

    moveToRootProjects() {
        this.moveTo(rootNames.rootProjects);
    }

    moveToRootProjectsNew() {
        this.moveTo(rootNames.rootProjectsNew);
    }

    moveToRootAbout() {
        this.moveTo(rootNames.rootAbout);
    }
}
