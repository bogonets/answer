import {ReccApiBase} from '@/reccApiBase';
import type {VersionsA} from '@/packet/system';

export class ReccApiDevSystem extends ReccApiBase {
  getDevSystemVersions() {
    return this.get<VersionsA>('/dev/system/versions');
  }
}
