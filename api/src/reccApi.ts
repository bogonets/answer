import ReccApiBase from '@/reccApiBase';
import {applyMixins} from '@/mixin';
import {ReccApiPublic} from '@/mixins/public';
import {ReccApiSelf} from '@/mixins/self';
import type {ReccApiOptions} from '@/reccApiBase';

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

interface ReccApi extends ReccApiPublic, ReccApiSelf {
  // EMPTY.
}
applyMixins(ReccApi, [ReccApiPublic, ReccApiSelf]);

export default ReccApi;
