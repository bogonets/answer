import {ReccApiBase} from '../../reccApiBase';
import type {EnvironmentA} from '../../packet/environment';

export class ReccApiDevEnvironments extends ReccApiBase {
  getDevEnvironments() {
    return this.get<Array<EnvironmentA>>('/dev/environments');
  }
}
