<template>
  <v-container class="project-main">
    <adr-navigation v-if="enableLegacy">
    </adr-navigation>

    <adr-components>
    </adr-components>

    <adlg-add-layout>
    </adlg-add-layout>

    <router-view>
    </router-view>
  </v-container>
</template>

<script lang='ts'>
import adrNavigation from '@/components/Drawer/adrNavigation.vue';
import adrComponents from '@/components/Drawer/adrComponents.vue';
import adlgAddLayout from '@/components/Dialog/adlgAddLayout.vue';
import { Component, Prop } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component({
  components: {
    adrNavigation,
    adrComponents,
    adlgAddLayout,
  }
})
export default class ProjectPage extends VueBase {

  @Prop({type: String, default: ''})
  readonly group!: string;

  @Prop({type: String, default: ''})
  readonly project!: string;

  enableLegacy = true;

  mounted() {
    if (this.enableLegacy) {
      this.$store.commit('drawer/setNaviShow', {bool: true});
      this.$store.commit('project/setSelectProject', {name: '[Project Name]'});
      this.$store.commit('project/setViewNaviList', {menus: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]});
      this.$store.commit('signal/setLayoutMainSignal', {bool: true});
    }
  }

  beforeDestroy() {
    if (this.enableLegacy) {
      this.$store.commit('drawer/setNaviShow', {bool: false});
      this.$store.commit('project/setViewNaviList', {menus: null});
    }
  }
}
</script>
