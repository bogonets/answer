<template>
  <v-app-bar app dense fixed clipped-left clipped-right>
    <v-btn plain small @click="moveDashboard">
      <title-logo-small></title-logo-small>
    </v-btn>
    <v-btn plain small text color="primary" @click="moveProjects">
      {{ $t('main.projects') }}
    </v-btn>
    <v-btn plain small text disabled color="primary" @click="moveGroups">
      {{ $t('main.groups') }}
    </v-btn>

    <v-spacer></v-spacer>

    <menu-account></menu-account>
  </v-app-bar>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import MenuAccount from '@/components/MenuAccount.vue';
import TitleLogoSmall from "@/components/TitleLogoSmall.vue";

@Component({
  components: {
    TitleLogoSmall,
    MenuAccount,
  }
})
export default class MainTitleBar extends Vue {

  moveDashboard() {
    // EMPTY.
  }

  moveProjects() {
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
