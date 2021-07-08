import { localStore } from "./store/index";

declare module "vue/types/vue" {
  interface Vue {
    $localStore: localStore;
  }
}