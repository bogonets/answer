import {Vue, Component} from 'vue-property-decorator';
import {RawLocation} from 'vue-router';
import {Dictionary} from 'vue-router/types/router';
import _ from 'lodash';

type ParamsType = Dictionary<string>;
type QueryType = Dictionary<string | (string | null)[] | null | undefined>;

@Component
export default class Router extends Vue {
  moveToBack() {
    this.$router.back();
  }

  moveTo(name: string, params?: ParamsType, query?: QueryType) {
    if (this.$router.currentRoute.name === name) {
      const paramsEqual = _.isEqual(params, this.$router.currentRoute.params);
      const queryEqual = _.isEqual(query, this.$router.currentRoute.query);
      if (paramsEqual && queryEqual) {
        return;
      }
    }

    const rawLocation = {
      name: name,
      params: params,
      query: query,
    } as RawLocation;

    this.$router.push(rawLocation).catch((reason: any) => {
      if (reason.name !== 'NavigationDuplicated') {
        throw reason;
      }
    });
  }
}
