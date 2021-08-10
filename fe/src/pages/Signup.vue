<template>
  <v-content>
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col>
          <af-signup-form
              @close="onClose"
              @success="onSuccess"
          ></af-signup-form>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import afSignupForm from '@/components/Form/afSignupForm.vue';

@Component({
  components: {
    afSignupForm,
  },
})
export default class Signup extends VueBase {
  onClose() {
    this.moveToSignin();
  }

  onSuccess() {
    this.moveToSignin();
  }
}
</script>
