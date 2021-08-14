<template>
  <div>
    <p v-if="!!label" class="text-subtitle-2 font-weight-bold mb-1">
      {{ label }}
    </p>

    <slot></slot>

    <p v-if="!!hint" class="text-caption mt-1">
      {{ hint }}
    </p>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class TextFieldThreeLine extends Vue {
  @Prop({type: String, default: ''})
  readonly label!: string;

  @Prop({type: String, default: ''})
  readonly hint!: string;
}
</script>
