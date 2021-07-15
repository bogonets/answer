import { Store } from "vuex";

declare module "vue/types/vue" {
  interface Vue {
    $localStore: Store<any>;
  }
}
