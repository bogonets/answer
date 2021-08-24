<template>
  <v-app>
    <main-title-bar>
    </main-title-bar>

    <v-main>
      <navi-admin
          default-behavior
      ></navi-admin>

      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MainTitleBar from '@/components/MainTitleBar.vue';
import NaviAdmin from '@/pages/navigation/NaviAdmin.vue';

@Component({
  components: {
    MainTitleBar,
    NaviAdmin,
  }
})
export default class Admin extends VueBase {
}
</script>
