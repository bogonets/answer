<template>
  <v-app>
    <adr-navigation>
    </adr-navigation>

    <adr-components>
    </adr-components>

    <atb-title-bar>
    </atb-title-bar>

    <v-main>
      <adlg-add-layout />
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import adrNavigation from "@/components/Drawer/adrNavigation";
import adrComponents from "@/components/Drawer/adrComponents";
import atbTitleBar from "@/components/Titlebar/atbTitleBar";
import adlgAddLayout from "@/components/Dialog/adlgAddLayout";

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
    this.$router.push(this.$page.projects);
  }
}
</script>
