<template>
  <v-container>
    <navi-admin
        default-behavior
    ></navi-admin>

    <router-view>
    </router-view>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import NaviAdmin from '@/pages/navigation/NaviAdmin.vue';

@Component({
  components: {
    NaviAdmin
  }
})
export default class MainAdmin extends VueBase {
}
</script>
