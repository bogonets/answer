<i18n lang="yaml">
en:
  label:
    uid: "Airjoy ID"
    name: "Name"
    description: "Description"
  hint:
    uid: "Please check the Airjoy serial number you purchased"
    name: "The name of the Airjoy that will be displayed on the screen"
    description: "Details field for users"
  name: "Name"
  value: "Value"
  cancel: "Cancel"
  ok: "Ok"

ko:
  label:
    uid: "에어조이 ID"
    name: "이름"
    description: "상세 설명"
  hint:
    uid: "구매한 에어조이 시리얼넘버를 확인해 주세요"
    name: "화면에 표시될 에어조이 명칭 입니다"
    description: "사용자를 위한 세부 정보 입니다"
  name: "이름"
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
                v-model="uid"
                :rules="uidRules"
                :label="$t('label.uid')"
                :hint="$t('hint.uid')"
            ></v-text-field>
          </v-list-item>

          <v-list-item>
            <v-text-field
                dense
                outlined
                v-model="name"
                :rules="nameRules"
                :label="$t('label.name')"
                :hint="$t('hint.name')"
            ></v-text-field>
          </v-list-item>

          <v-list-item>
            <v-textarea
                dense
                outlined
                v-model="description"
                :label="$t('label.description')"
                :hint="$t('hint.description')"
            ></v-textarea>
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
          :loading="submitLoading"
          color="primary"
          @click="submit"
      >
        {{ $t('ok') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import requiredField from '@/rules/required';
import {DEFAULT_CHART_COLOR} from "@/packet/airjoy";
import type {AirjoyCreateDeviceQ} from '@/packet/airjoy';
import {UID_RULES} from "@/rules";

@Component
export default class AirjoyDeviceAdd extends VueBase {
  private readonly uidRules = UID_RULES;
  private readonly nameRules = [requiredField];

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean, default: false})
  readonly submitLoading!: boolean;

  valid = false;
  uid = '';
  name = '';
  description = '';

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
  }

  @Emit()
  ok() {
    return {
      name: this.name,
      uid: Number.parseInt(this.uid),
      description: this.description,
      chart_color: DEFAULT_CHART_COLOR,
    } as AirjoyCreateDeviceQ;
  }
}
</script>
