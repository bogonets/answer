<template>
  <v-app>
    <bar-main>
    </bar-main>

    <v-main>
      <navi-group>
      </navi-group>

      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import NaviGroup from "@/pages/navigation/NaviGroup.vue";

@Component({
  components: {
    BarMain,
    NaviGroup,
  }
})
export default class RouterBarMainNaviGroup extends VueBase {
}
</script>
