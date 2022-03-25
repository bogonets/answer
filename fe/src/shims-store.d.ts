import {LocalStore} from '@/store/localStore';
import {SessionStore} from '@/store/sessionStore';

declare module 'vue/types/vue' {
  interface Vue {
    $localStore: LocalStore;
    $sessionStore: SessionStore;
  }
}
