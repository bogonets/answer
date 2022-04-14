import {ReccApiBase} from '../../reccApiBase';
import type {PluginA} from '../../packet/plugin';

export class ReccApiDevPlugins extends ReccApiBase {
  getDevPlugins() {
    return this.get<Array<PluginA>>('/dev/plugins');
  }
}
