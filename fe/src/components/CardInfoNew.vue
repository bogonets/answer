<i18n lang="yaml">
en:
  key: "Key"
  value: "Value"
  cancel: "Cancel"
  ok: "Ok"

ko:
  key: "열쇠 (Key)"
  value: "값 (Value)"
  cancel: "취소"
  ok: "확인"
</i18n>

<template>
  <v-card>
    <v-card-title class="mb-1">{{ title }}</v-card-title>
    <v-card-subtitle>{{ subtitle }}</v-card-subtitle>

    <v-divider></v-divider>

    <v-container>
      <v-form
          ref="form"
          v-model="valid"
          lazy-validation
      >
        <v-list flat>
          <v-list-item>
            <v-text-field
                dense
                outlined
                type="text"
                autocomplete="off"
                v-model="infoKey"
                :filled="disableKey"
                :disabled="disableKey"
                :rules="infoRules"
                :label="$t('key')"
            ></v-text-field>
          </v-list-item>
          <v-list-item>
            <v-text-field
                dense
                outlined
                hide-details
                type="text"
                autocomplete="off"
                v-model="infoValue"
                :label="$t('value')"
                @keydown.enter.stop="submit"
            ></v-text-field>
          </v-list-item>
        </v-list>
      </v-form>
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
          @click="submit"
      >
        {{ $t('ok') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import {Component, Prop, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {INFO_RULES} from '@/rules';

@Component
export default class CardInfoNew extends VueBase {
  private readonly infoRules = INFO_RULES;

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly disableKey!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

  @Prop({type: String, default: ''})
  readonly initKey!: string;

  @Prop({type: String, default: ''})
  readonly initValue!: string;

  valid = false;
  infoKey = '';
  infoValue = '';

  mounted() {
    this.infoKey = this.initKey;
    this.infoValue = this.initValue;
  }

  @Watch('initKey')
  onWatchInitKey(value) {
    this.infoKey = value;
  }

  @Watch('initValue')
  onWatchInitValue(value) {
    this.infoValue = value;
  }

  get form() {
    return this.$refs.form;
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
    return {
      key: this.infoKey,
      value: this.infoValue,
    };
  }

  @Emit()
  ok() {
    return {
      key: this.infoKey,
      value: this.infoValue,
    };
  }
}
</script>
