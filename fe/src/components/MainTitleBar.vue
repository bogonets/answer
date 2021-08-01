<i18n lang="yaml">
en:
  projects: "Projects"
  groups: "Groups"

ko:
  projects: "Projects"
  groups: "Groups"
</i18n>

<template>
  <v-app-bar app dense fixed clipped-left clipped-right>
    <v-btn plain small @click="moveDashboard">
      <title-logo-small></title-logo-small>
    </v-btn>
    <v-btn plain small text color="primary" @click="moveProjects">
      {{ $t('projects') }}
    </v-btn>
    <v-btn plain small text disabled color="primary" @click="moveGroups">
      {{ $t('groups') }}
    </v-btn>

    <v-spacer></v-spacer>

    <menu-account></menu-account>
  </v-app-bar>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MenuAccount from '@/components/MenuAccount.vue';
import TitleLogoSmall from "@/components/TitleLogoSmall.vue";

@Component({
  components: {
    TitleLogoSmall,
    MenuAccount,
  }
})
export default class MainTitleBar extends VueBase {

  moveDashboard() {
    // EMPTY.
  }

  moveProjects() {
    this.moveToMainProjects();
    const location = '/main/projects';
    if (this.$router.currentRoute.path !== location) {
      this.$router.push(location);
    }
  }

  moveGroups() {
    // EMPTY.
  }
}
</script>
