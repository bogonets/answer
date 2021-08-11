<template>
  <div>
    <p v-if="!hideLabel" class="text-subtitle-2 font-weight-bold mb-1">
      {{ label }}
    </p>

    <v-text-field
        dense
        outlined
        hide-details
        :disabled="disabled"
        :filled="disabled"
        :type="type"
        :autocomplete="autocomplete"
        :value="value"
        @input="onInputText"
    ></v-text-field>

    <p v-if="!hideHint" class="text-caption mt-1">
      {{ hint }}
    </p>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class TextFieldThreeLine extends Vue {
  @Prop({type: Boolean, default: false})
  readonly disabled!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideLabel!: boolean;

  @Prop({type: String, default: ''})
  readonly label!: string;

  @Prop({type: Boolean, default: false})
  readonly hideHint!: boolean;

  @Prop({type: String, default: ''})
  readonly hint!: string;

  @Prop({type: String, default: 'text'})
  readonly type!: string;

  @Prop({type: String, default: 'off'})
  readonly autocomplete!: string;

  @Prop({type: String, default: ''})
  readonly value!: string;

  onInputText(value) {
    this.$emit('input', value);
  }
}
</script>
