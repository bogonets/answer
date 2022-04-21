import Component, {mixins} from 'vue-class-component';
import Toast from '@/base/mixin/Toast';
import WatchI18n from '@/base/mixin/WatchI18n';
import RouterAdmin from '@/base/router/RouterAdmin';
import RouterDev from '@/base/router/RouterDev';
import RouterGroup from '@/base/router/RouterGroup';
import RouterMain from '@/base/router/RouterMain';
import RouterRoot from '@/base/router/RouterRoot';
import RouterSelf from '@/base/router/RouterSelf';
import StorePermission from '@/base/store/StorePermission';

@Component
export default class VueBase extends mixins(
  Toast,
  WatchI18n,
  RouterAdmin,
  RouterDev,
  RouterGroup,
  RouterMain,
  RouterRoot,
  RouterSelf,
  StorePermission,
) {
  getOem() {
    return this.$localStore.preference.oem;
  }

  hasAdmin() {
    return this.$localStore.user.is_admin || false;
  }

  moveToMainGroups() {}

  moveToMainProjects() {}

  moveToMainProjectsNew() {}

  moveToMainProject(group?: string, project?: string) {}
}
