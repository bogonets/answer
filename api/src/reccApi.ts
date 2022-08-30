import ReccApiBase from './reccApiBase';
import {applyMixins} from './mixin';
import {ReccApiAdminConfigs} from './mixins/admin/configs';
import {ReccApiAdminContainers} from './mixins/admin/containers';
import {ReccApiAdminGroups} from './mixins/admin/groups';
import {ReccApiAdminPlugin} from './mixins/admin/plugin';
import {ReccApiAdminProjects} from './mixins/admin/projects';
import {ReccApiAdminRoles} from './mixins/admin/roles';
import {ReccApiAdminSystem} from './mixins/admin/system';
import {ReccApiAdminTemplates} from './mixins/admin/templates';
import {ReccApiAdminUsers} from './mixins/admin/users';
import {ReccApiDevConfigs} from './mixins/dev/configs';
import {ReccApiDevInfos} from './mixins/dev/infos';
import {ReccApiDevPlugins} from './mixins/dev/plugins';
import {ReccApiDevSystem} from './mixins/dev/system';
import {ReccApiMainGroups} from './mixins/main/groups';
import {ReccApiMainInfos} from './mixins/main/infos';
import {ReccApiMainPermissions} from './mixins/main/permissions';
import {ReccApiMainProjects} from './mixins/main/projects';
import {ReccApiMainRoles} from './mixins/main/roles';
import {ReccApiPublic} from './mixins/public';
import {ReccApiSelf} from './mixins/self';
import type {ReccApiOptions} from './reccApiBase';

class ReccApi extends ReccApiBase {
  constructor(options?: ReccApiOptions) {
    super(options);
  }

  private static globalInstance?: ReccApi;

  static get global(): ReccApi {
    if (!ReccApi.globalInstance) {
      ReccApi.globalInstance = new ReccApi();
    }
    return ReccApi.globalInstance as ReccApi;
  }
}

interface ReccApi
  extends ReccApiAdminConfigs,
    ReccApiAdminContainers,
    ReccApiAdminGroups,
    ReccApiAdminPlugin,
    ReccApiAdminProjects,
    ReccApiAdminRoles,
    ReccApiAdminSystem,
    ReccApiAdminTemplates,
    ReccApiAdminUsers,
    ReccApiDevConfigs,
    ReccApiDevInfos,
    ReccApiDevPlugins,
    ReccApiDevSystem,
    ReccApiMainGroups,
    ReccApiMainInfos,
    ReccApiMainPermissions,
    ReccApiMainProjects,
    ReccApiMainRoles,
    ReccApiPublic,
    ReccApiSelf {
  // EMPTY.
}
applyMixins(ReccApi, [
  ReccApiAdminConfigs,
  ReccApiAdminContainers,
  ReccApiAdminGroups,
  ReccApiAdminPlugin,
  ReccApiAdminProjects,
  ReccApiAdminRoles,
  ReccApiAdminSystem,
  ReccApiAdminTemplates,
  ReccApiAdminUsers,
  ReccApiDevConfigs,
  ReccApiDevInfos,
  ReccApiDevPlugins,
  ReccApiDevSystem,
  ReccApiMainGroups,
  ReccApiMainInfos,
  ReccApiMainPermissions,
  ReccApiMainProjects,
  ReccApiMainRoles,
  ReccApiPublic,
  ReccApiSelf,
]);

export default ReccApi;
