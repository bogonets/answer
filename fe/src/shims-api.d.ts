import ApiV2 from "@/apis/api-v2";

declare module 'vue/types/vue' {
  interface Vue {
    $api2: ApiV2;
  }
}
