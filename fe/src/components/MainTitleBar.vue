<template>
  <v-app-bar app dense fixed clipped-left clipped-right>
    <v-btn plain small @click="moveProjects">
      <title-logo-small></title-logo-small>
    </v-btn>
    <v-btn plain small text color="primary" @click="moveProjects">
      {{ $t('main.projects') }}
    </v-btn>
    <v-btn plain small text disabled color="primary" @click="moveGroups">
      {{ $t('main.groups') }}
    </v-btn>

    <v-spacer></v-spacer>

    <v-btn v-if="hasAdminPermission" icon @click="moveAdminArea">
      <v-icon role="img">{{ icons.cogBox }}</v-icon>
    </v-btn>
    <adb-user-box></adb-user-box>
  </v-app-bar>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { mdiCogBox } from '@mdi/js';
import adbUserBox from '@/components/Dropbox/adbUserBox.vue';
import TitleLogoSmall from "@/components/TitleLogoSmall.vue";

@Component({
  components: {
    TitleLogoSmall,
    adbUserBox,
  }
})
export default class MainTitleBar extends Vue {

  private readonly icons = {
    cogBox: mdiCogBox,
  };

  get hasAdminPermission(): boolean {
    return true;
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

  moveAdminArea() {
    // this.$router.push('/main/admin');
  }
}
</script>
