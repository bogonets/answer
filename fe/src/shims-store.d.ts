import {LocalStore} from '@/store/LocalStore';
import {SessionStore} from '@/store/SessionStore';

declare module 'vue/types/vue' {
  interface Vue {
    $localStore: LocalStore;
    $sessionStore: SessionStore;
  }
}
