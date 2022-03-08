<i18n lang="yaml">
en:
  tab:
    info: "Information"
    env: "Environment"
    log: "Logging"

ko:
  tab:
    info: "정보"
    env: "환경"
    log: "로그"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-tabs>
      <v-tab to="info">{{ $t('tab.info') }}</v-tab>
      <v-tab to="env">{{ $t('tab.env') }}</v-tab>
      <v-tab to="log">{{ $t('tab.log') }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>

    <router-view>
    </router-view>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class AdminDaemonsEdit extends VueBase {
  readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Daemons',
      disabled: false,
      href: () => this.moveToAdminDaemons(),
    },
    {
      text: 'Edit',
      disabled: true,
    },
    {
      text: this.$route.params.daemon,
      disabled: true,
    },
  ];
}
</script>
