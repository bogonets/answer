<template>
  <v-app>
    <atb-title-bar>
    </atb-title-bar>

    <adr-navigation>
    </adr-navigation>

    <adr-components>
    </adr-components>

    <v-main>
      <adlg-add-layout>
      </adlg-add-layout>

      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import adrNavigation from '@/components/Drawer/adrNavigation.vue';
import adrComponents from '@/components/Drawer/adrComponents.vue';
import atbTitleBar from '@/components/Titlebar/atbTitleBar.vue';
import adlgAddLayout from '@/components/Dialog/adlgAddLayout.vue';

@Component({
  components: {
    atbTitleBar,
    adrNavigation,
    adrComponents,
    adlgAddLayout,
  }
})
export default class MainPage extends Vue {
  mounted() {
    this.$router.push('/main/projects');
  }
}
</script>
