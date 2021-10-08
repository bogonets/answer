<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator'
import VueBase from '@/base/VueBase';
import {onLoadSession} from '@/event/session';

@Component
export default class App extends VueBase {
  created() {
    onLoadSession(this);
  }
}
</script>
