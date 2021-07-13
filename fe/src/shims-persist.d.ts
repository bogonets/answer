import PersistBase from '@/persists/PersistBase.ts';

declare module 'vue/types/vue' {
  interface Vue {
    $persist: PersistBase;
  }
}
