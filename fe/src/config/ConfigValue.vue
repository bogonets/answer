<template>
  <div class="config-layout">
    <v-text-field
        v-if="!isBoolean"
        dense
        outlined
        hide-details
        type="text"
        autocomplete="off"
        :disabled="disable"
        :value="value"
        @input="input"
        :label="label"
        @keydown.esc.stop="esc"
        @keydown.enter.stop="enter"
    ></v-text-field>
    <v-switch
        v-if="isBoolean"
        inset
        hide-details
        :disabled="disable"
        :value="toBoolean"
        :label="label"
        @change="input"
    ></v-switch>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

type ValueType = '' | 'str' | 'bool' | 'int' | 'float';

@Component
export default class ConfigValue extends VueBase {
  @Prop({type: String, default: ''})
  readonly type!: ValueType;

  @Prop({type: String, default: ''})
  readonly value!: string;

  @Prop({type: String, default: ''})
  readonly label!: string;

  @Prop({type: Boolean, default: false})
  readonly disable!: boolean;

  get isString() {
    return this.type === '' || this.type === 'str';
  }

  get isBoolean() {
    return this.type === 'bool';
  }

  get isInteger() {
    return this.type === 'int';
  }

  get isFloating() {
    return this.type === 'float';
  }

  get toBoolean() {
    const value = this.value?.toLowerCase() || '';
    return value === 'true';
  }

  get toInteger() {
    return Number.parseInt(this.value);
  }

  get toFloating() {
    return Number.parseFloat(this.value);
  }

  @Emit('input')
  input(value: any) {
    if (this.isBoolean) {
      return value ? 'True' : 'False';
    }

    if (typeof value === 'undefined') {
      return '';
    } else {
      return value.toString();
    }
  }

  @Emit('esc')
  esc() {
  }

  @Emit('enter')
  enter() {
  }
}
</script>

<style lang="scss" scoped>
.config-layout {
  width: 100%;
  height: 100%;
}
</style>
