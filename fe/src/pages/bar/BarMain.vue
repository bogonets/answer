<i18n lang="yaml">
en:
  projects: 'Projects'
  groups: 'Groups'

ko:
  projects: 'Projects'
  groups: 'Groups'
</i18n>

<template>
  <v-app-bar class="app-bar" app dense fixed clipped-left clipped-right>
    <v-btn plain small @click="onClickLogo">
      <title-logo-small></title-logo-small>
    </v-btn>

    <v-btn plain small text color="primary" @click="onClickGroups">
      {{ $t('groups') }}
    </v-btn>

    <v-btn plain small text color="primary" @click="onClickProjects">
      {{ $t('projects') }}
    </v-btn>

    <v-spacer></v-spacer>

    <v-btn icon>
      <v-icon>mdi-bell</v-icon>
    </v-btn>

    <menu-account></menu-account>
  </v-app-bar>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MenuAccount from '@/components/MenuAccount.vue';
import TitleLogoSmall from '@/components/TitleLogoSmall.vue';

@Component({
  components: {
    TitleLogoSmall,
    MenuAccount,
  },
})
export default class BarMain extends VueBase {
  onClickLogo() {
    this.moveToRoot();
  }

  onClickGroups() {
    this.moveToRootGroups();
  }

  onClickProjects() {
    this.moveToRootProjects();
  }
}
</script>

<style lang="scss" scoped>
.app-bar {
  z-index: 9999;
}
</style>
