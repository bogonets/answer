<template>
  <v-container>
  </v-container>
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
export default class Root extends VueBase {
  created() {
    if (!this.$localStore.alreadySession) {
      this.moveToSignin();
      return;
    }
  }
}
</script>
