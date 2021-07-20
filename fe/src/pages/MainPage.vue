<template>
  <v-app>
    <main-title-bar>
    </main-title-bar>

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
import MainTitleBar from '@/components/MainTitleBar.vue';
import adlgAddLayout from '@/components/Dialog/adlgAddLayout.vue';

@Component({
  components: {
    MainTitleBar,
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
