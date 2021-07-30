<template>
  <v-container>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class UserEditPage extends VueBase {
  @Prop({type: String, default: ''})
  readonly username!: string;

  mounted() {
    console.debug(`Username: ${this.username}`);
  }
}
</script>
