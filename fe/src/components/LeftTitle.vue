<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <v-card flat color="transparent">
          <v-card-title>
            {{ header }}
          </v-card-title>
          <v-card-subtitle>
            {{ subheader }}
          </v-card-subtitle>
        </v-card>
      </v-col>

      <v-col cols="8">
        <v-card flat color="transparent">
          <v-card-text>
            <slot></slot>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class LeftTitle extends Vue {
  @Prop({type: String, default: ''})
  readonly header!: string;

  @Prop({type: String, default: ''})
  readonly subheader!: string;
}
</script>
