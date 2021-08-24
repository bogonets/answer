<template>
  <v-app>
    <bar-main>
    </bar-main>

    <v-main>
      <!--<navi-dev
          default-behavior
      ></navi-dev>-->

      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';

@Component({
  components: {
    BarMain,
  }
})
export default class Dev extends VueBase {
}
</script>
