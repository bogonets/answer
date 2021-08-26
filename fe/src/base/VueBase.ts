import Component, {mixins} from 'vue-class-component';
import Toast from '@/base/mixin/Toast';
import WatchI18n from '@/base/mixin/WatchI18n';
import RouterAdmin from '@/base/router/RouterAdmin';
import RouterDev from '@/base/router/RouterDev';
import RouterGroup from "@/base/router/RouterGroup";
import RouterRoot from '@/base/router/RouterRoot';
import RouterSelf from '@/base/router/RouterSelf';

@Component
export default class VueBase extends mixins(
    Toast,
    WatchI18n,
    RouterAdmin,
    RouterDev,
    RouterGroup,
    RouterRoot,
    RouterSelf,
) {
    moveToMainGroups() {
    }

    moveToMainProjects() {
    }

    moveToMainProjectsNew() {
    }

    moveToMainProject(group?: string, project?: string) {
    }
}
