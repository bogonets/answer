import Vue from 'vue'
import { REST_API } from "@/services/api";
import ApiV2 from "@/apis";

declare module 'vue/types/vue' {
  interface Vue {
    $api: REST_API;
    $api2: ApiV2;
  }
}
