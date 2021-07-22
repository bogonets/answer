import Vue from 'vue'
import { Versions } from '@/versions';

declare module 'vue/types/vue' {
  interface Vue {
    $versions: Versions;
  }
}
