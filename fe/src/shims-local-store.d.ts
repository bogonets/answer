import { LocalStore } from '@/store/LocalStore';

declare module 'vue/types/vue' {
  interface Vue {
    $localStore: LocalStore;
  }
}
