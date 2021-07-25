<template>
  <v-app-bar :flat="flat">
    <v-app-bar-title>
      {{ title }}
    </v-app-bar-title>
    <template v-if="!!subtitle" v-slot:extension>
      <p class="text--secondary">
        {{ subtitle }}
      </p>
    </template>
  </v-app-bar>
</template>

<script lang="ts">
import VueI18n from '@/translations/VueI18n';
import { Component, Prop } from 'vue-property-decorator';

@Component
export default class AppBarTitle extends VueI18n {

  @Prop({type: Boolean, default: false})
  readonly flat!: boolean;

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;
}
</script>
