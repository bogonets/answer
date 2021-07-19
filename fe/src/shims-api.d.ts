import Vue from 'vue'
import { REST_API } from "@/apis/api";
import ApiV2 from "@/apis/api-v2";

declare module 'vue/types/vue' {
  interface Vue {
    $api: REST_API;
    $api2: ApiV2;
  }
}
