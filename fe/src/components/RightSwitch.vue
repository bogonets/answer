<template>
  <right-control
      :title="title"
      :subtitle="subtitle"
  >
    <v-switch
        :inset="inset"
        :value="value"
        @change="onChange"
    ></v-switch>
  </right-control>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';
import RightControl from "@/components/RightControl.vue";

@Component({
  components: {
    RightControl,
  },
})
export default class RightSwitch extends Vue {
  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly inset!: boolean;

  @Prop({type: Boolean})
  readonly value!: boolean;

  onChange(value: boolean | null) {
    this.$emit('input', !!value);
  }
}
</script>
