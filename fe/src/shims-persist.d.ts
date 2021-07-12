import Persist from '@/persists/persist.ts';

declare module 'vue/types/vue' {
  interface Vue {
    $persist: Persist;
  }
}
