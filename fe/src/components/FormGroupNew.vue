<i18n lang="yaml">
en:
  header:
    basic: "Basic information"
    detail: "Detail information"
  label:
    name: "Name"
    description: "Password"
    features: "Confirm"
  hint:
    name: "The group name to be displayed on the screen."
    description: "A specific description of the group."
    features: "The function to be applied to the group."
  cancel: "Cancel"
  create: "Create"

ko:
  header:
    basic: "기본 정보"
    detail: "상세 정보"
  label:
    name: "이름"
    description: "비밀번호"
    features: "비밀번호 확인"
  hint:
    name: "화면에 표시될 그룹 명칭."
    description: "그룹의 구체적인 설명."
    features: "그룹에 적용할 기능 목록 입니다."
  cancel: "취소"
  create: "생성"
</i18n>

<template>
  <v-form
      ref="form"
      v-model="valid"
  >
    <v-subheader v-if="!hideSubheader">{{ $t('header.required') }}</v-subheader>
    <v-divider v-if="!hideSubheader"></v-divider>
    <v-list flat>
      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-account-group"
            v-model="name"
            :rules="rules.name"
            :label="$t('label.name')"
            :hint="$t('hint.name')"
        ></v-text-field>
      </v-list-item>
    </v-list>

    <v-subheader v-if="!hideDetail && !hideSubheader">{{ $t('header.detail') }}</v-subheader>
    <v-divider v-if="!hideDetail && !hideSubheader"></v-divider>
    <v-list v-if="!hideDetail" flat>
      <v-list-item>
        <v-textarea
            :label="$t('label.description')"
            auto-grow
            outlined
            filled
        ></v-textarea>
      </v-list-item>

      <v-list-item>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-phone"
            v-model="phone1"
            :rules="rules.phone"
            :label="$t('label.phone1')"
            :hint="$t('hint.phone1')"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-phone"
            v-model="phone2"
            :rules="rules.phone"
            :label="$t('label.phone2')"
            :hint="$t('hint.phone2')"
        ></v-text-field>
      </v-list-item>
    </v-list>

    <v-subheader v-if="!hideAccess && !hideSubheader">{{ $t('header.access') }}</v-subheader>
    <v-divider v-if="!hideAccess && !hideSubheader"></v-divider>
    <v-list v-if="!hideAccess" flat>
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('label.is_admin') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('hint.is_admin') }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-switch inset v-model="isAdmin"></v-switch>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list flat>
      <v-list-item :three-line="!denseFooter">
        <v-spacer></v-spacer>
        <v-btn
            color="second"
            class="mr-4"
            @click="cancel"
        >
          {{ $t('cancel') }}
        </v-btn>
        <v-btn
            color="primary"
            :loading="loading"
            :disabled="disableSubmit"
            @click="submit"
        >
          {{ $t('Create') }}
        </v-btn>
      </v-list-item>
    </v-list>
  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {Group} from '@/apis/api-v2';
import {GROUP_NAME_RULES} from '@/rules';

@Component
export default class FormGroupNew extends VueBase {
  private readonly rules = {
    name: GROUP_NAME_RULES,
  };

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideDetail!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideSubheader!: boolean;

  @Prop({type: Boolean, default: false})
  readonly denseFooter!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

  valid = false;
  name = '';
  description = '';
  features: Array<string> = [];
  isAdmin = false;

  get disableSubmit(): boolean {
    return this.loading || !this.valid;
  }

  get form() {
    return this.$refs.form;
  }

  validate() {
    this.form['validate']();
  }

  reset() {
    this.form['reset']();
  }

  resetValidation() {
    this.form['resetValidation']();
  }

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit()
  ok() {
    const required = {
      name: this.name,
    };
    const detail = {
      description: this.description,
      features: this.features,
    };

    return {
      ... required,
      ... (this.hideDetail ? undefined : detail),
    } as Group;
  }

  submit() {
    if (!this.disableValidate) {
      this.validate();
      if (!this.valid) {
        return;
      }
    }

    this.ok();
  }
}
</script>
