<template>
  <v-content>
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col xs12 sm8 md6>
          <v-signup-admin></v-signup-admin>
        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import vSignupAdmin from "@/components/Form/afSignupAdmin.vue"

@Component({
  components: {
    vSignupAdmin,
  },
})
export default class SignupAdmin extends VueBase {
}
</script>
