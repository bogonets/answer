<template>
  <div class="d-flex">
    <v-card flat color="transparent">
      <v-card-text class="pa-0">
        <p class="text-subtitle-2 font-weight-bold mb-2">
          {{ title }}
        </p>
        <p class="text-caption mt-2">
          {{ subtitle }}
        </p>
      </v-card-text>
    </v-card>
    <v-card flat color="transparent" class="ml-auto">
      <slot></slot>
    </v-card>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class RightControl extends Vue {
  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;
}
</script>
