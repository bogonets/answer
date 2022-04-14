import {ReccApiBase} from '@/reccApiBase';

export class ReccApiMainPermissions extends ReccApiBase {
  getMainPermissions() {
    return this.get<Array<string>>('/main/permissions');
  }
}
