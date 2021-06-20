import Vue from 'vue'

declare module 'vue/types/vue' {
  interface Vue {
    $debug: (filename, methods, ...args) => void;
    $info: (filename, methods, ...args) => void;
    $warn: (filename, methods, ...args) => void;
    $error: (filename, methods, ...args) => void;
  }
}