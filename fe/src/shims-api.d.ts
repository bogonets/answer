import Vue from 'vue'
import { REST_API } from "./services/api";

declare module 'vue/types/vue' {
  interface Vue {
    $api: REST_API;
  }
}
