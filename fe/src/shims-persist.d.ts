import PersistBase from '@/persists/persist-base.ts';

declare module 'vue/types/vue' {
  interface Vue {
    $persist: PersistBase;
  }
}
