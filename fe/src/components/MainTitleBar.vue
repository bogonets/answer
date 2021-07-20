<template>
  <v-app-bar app dense fixed clipped-left clipped-right>
    <!--<v-app-bar-nav-icon @click.stop="openMenu"></v-app-bar-nav-icon>-->
    <v-btn text color="primary" @click="moveProjects" >projects</v-btn>
    <v-spacer></v-spacer>
    <v-btn v-if="hasAdminPermission" icon @click="moveAdminArea">
      <v-icon role="img" aria-hidden="false">{{ icons.cogBox }}</v-icon>
    </v-btn>
    <adb-user-box></adb-user-box>
  </v-app-bar>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { mdiCogBox } from '@mdi/js';
import adbUserBox from '@/components/Dropbox/adbUserBox.vue';

@Component({
  components: {
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

  // openMenu() {
  //   if (this.$store.getters['drawer/getNaviWidth'] == 200) {
  //     this.$store.commit('drawer/setNaviWidth', { width: 55 });
  //   } else {
  //     this.$store.commit('drawer/setNaviWidth', { width: 200 });
  //   }
  // }

  moveProjects() {
    const location = '/main/projects';
    if (this.$router.currentRoute.path !== location) {
      this.$router.push(location);
    }
  }

  moveAdminArea() {
    // this.$router.push('/main/admin');
  }
}
</script>
