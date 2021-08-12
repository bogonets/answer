<template>
  <div>
    <h4 class="text-h4">{{ message }}</h4>
    <span class="text-body-2">{{ detail }}</span>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class SimpleToast extends Vue {
  @Prop({type: String, default: ''})
  readonly message!: string;

  @Prop({type: String, default: ''})
  readonly detail!: string;
}
</script>
