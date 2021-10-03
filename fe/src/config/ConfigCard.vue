<i18n lang="yaml">
en:
  title:
    new: "New Config"
    edit: "Edit Config"
  subtitle:
    new: "Create a new configuration"
    edit: "Modify an existing configuration"
  key: "Key"
  value: "Value"
  cancel: "Cancel"
  submit: "Submit"

ko:
  title:
    new: "새로운 구성"
    edit: "구성 편집"
  subtitle:
    new: "새로운 구성을 생성합니다"
    edit: "기존 구성을 수정합니다"
  key: "열쇠 (Key)"
  value: "값 (Value)"
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-card>
    <v-card-title class="mb-1">{{ titleText }}</v-card-title>
    <v-card-subtitle>{{ subtitleText }}</v-card-subtitle>

    <v-divider></v-divider>

    <v-form
        ref="form"
        v-model="valid"
        lazy-validation
    >
      <v-container>
        <v-list flat>
          <v-list-item>
            <v-text-field
                dense
                outlined
                type="text"
                autocomplete="off"
                :value="currentKey"
                @input="updateKey"
                :filled="disableKey"
                :disabled="disableKey"
                :rules="keyRules"
                :label="$t('key')"
                @keydown.esc.stop="cancel"
            ></v-text-field>
          </v-list-item>

          <v-list-item>
            <v-text-field
                dense
                outlined
                hide-details
                type="text"
                autocomplete="off"
                :value="currentValue"
                @input="updateValue"
                :label="$t('value')"
                @keydown.esc.stop="cancel"
                @keydown.enter.stop="submit"
            ></v-text-field>
          </v-list-item>
        </v-list>
      </v-container>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
            color="second"
            class="mr-1"
            @click="cancel"
        >
          {{ $t('cancel') }}
        </v-btn>

        <v-btn
            color="primary"
            :loading="loadingSubmit"
            :disabled="!enableSubmit"
            @click="submit"
        >
          {{ $t('ok') }}
        </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script lang="ts">
import {Component, Prop, Emit, Watch, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import requiredField from '@/rules/required';
import {ConfigA} from '@/packet/config';

type ModeType = '' | 'new' | 'edit';

@Component
export default class ConfigCard extends VueBase {
  private readonly keyRules = [requiredField];

  @Prop({type: String, default: ''})
  readonly mode!: ModeType;

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

  @Prop({type: String, default: ''})
  readonly configKey!: string;

  @Prop({type: String, default: ''})
  readonly configType!: string;

  @Prop({type: String, default: ''})
  readonly configValue!: string;

  @Prop({type: Boolean, default: false})
  readonly loadingSubmit!: boolean;

  @Ref()
  readonly form!: VForm;

  valid = false;

  originalKey = '';
  currentKey = '';

  originalType = '';
  currentType = '';

  originalValue = '';
  currentValue = '';

  mounted() {
    this.originalKey = this.configKey;
    this.originalType = this.configType;
    this.originalValue = this.configValue;

    this.currentKey = this.configKey;
    this.currentType = this.configType;
    this.currentValue = this.configValue;
  }

  @Watch('configKey')
  onWatchKey(newVal) {
    this.originalKey = newVal;
    this.currentKey = newVal;
  }

  @Watch('configType')
  onWatchType(newVal) {
    this.originalType = newVal;
    this.currentType = newVal;
  }

  @Watch('configValue')
  onWatchValue(newVal) {
    this.originalValue = newVal;
    this.currentValue = newVal;
  }

  get disableKey() {
    return this.mode === 'edit';
  }

  get modified() {
    if (this.currentKey !== this.originalKey) {
      return true;
    }
    return this.currentValue !== this.originalValue;
  }

  get enableSubmit() {
    return this.valid && this.modified && !this.loadingSubmit;
  }

  get titleText() {
    if (this.mode === 'new') {
      return this.$t('title.new').toString();
    } else if (this.mode === 'edit') {
      return this.$t('title.edit').toString();
    }
    return this.title.toString();
  }

  get subtitleText() {
    if (this.mode === 'new') {
      return this.$t('subtitle.new').toString();
    } else if (this.mode === 'edit') {
      return this.$t('subtitle.edit').toString();
    }
    return this.subtitle.toString();
  }

  @Emit('update:key')
  updateKey(value) {
    this.currentKey = value;
    return value;
  }

  @Emit('update:value')
  updateValue(value) {
    this.currentValue = value;
    return value;
  }

  formValidate() {
    this.form['validate']();
  }

  submit() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.ok();
  }

  @Emit()
  cancel() {
  }

  @Emit()
  ok() {
    return {
      key: this.currentKey,
      type: this.currentType,
      value: this.currentValue,
    } as ConfigA;
  }
}
</script>
