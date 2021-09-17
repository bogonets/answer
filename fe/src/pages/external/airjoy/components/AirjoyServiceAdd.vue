<i18n lang="yaml">
en:
  label:
    uid: "Airjoy ID"
    author: "Author"
    time: "Date/Time"
    description: "Description"
  hint:
    uid: "Please check the Airjoy serial number you purchased"
    author: "Author"
    time: "Date/Time"
    description: "Details field for users"
  name: "Name"
  value: "Value"
  cancel: "Cancel"
  ok: "Ok"

ko:
  label:
    uid: "에어조이 ID"
    author: "담당자"
    time: "날짜/시간"
    description: "상세 설명"
  hint:
    uid: "구매한 에어조이 시리얼넘버를 확인해 주세요"
    author: "Author"
    time: "Date/Time"
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
                v-model="uid"
                :label="$t('label.author')"
                :hint="$t('hint.author')"
            ></v-text-field>
          </v-list-item>

          <v-list-item>
            <v-text-field
                dense
                outlined
                v-model="name"
                :label="$t('label.time')"
                :hint="$t('hint.time')"
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
import type {CreateAirjoyDeviceQ} from '@/packet/airjoy';
import {UID_RULES} from "@/rules";

@Component
export default class AirjoyServiceAdd extends VueBase {
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
    } as CreateAirjoyDeviceQ;
  }
}
</script>
