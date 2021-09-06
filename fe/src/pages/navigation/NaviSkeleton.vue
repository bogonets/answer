<template>
  <v-navigation-drawer
      app
      clipped
      permanent
      stateless
      touchless
  >
    <v-skeleton-loader
        type="list-item-avatar,  divider, list-item, list-item, list-item"
    ></v-skeleton-loader>
  </v-navigation-drawer>
</template>

<script lang='ts'>
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class NaviSkeleton extends VueBase {
}
</script>
