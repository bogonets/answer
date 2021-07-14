import PersistRecc from "@/persists/PersistRecc.ts";

declare module 'vue/types/vue' {
  interface Vue {
    $persist: PersistRecc;
  }
}
