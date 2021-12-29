<i18n lang="yaml">
en:
  label:
    uid: "Airjoy ID"
    author: "Author"
    time: "Date/Time"
    description: "Description"
  hint:
    uid: "Please check the Airjoy serial number"
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
    uid: "에어조이 시리얼넘버를 확인해 주세요"
    author: "서비스 담당자 이름 입니다"
    time: "서비스 날짜 입니다"
    description: "제공된 서비스 상세 내역 입니다"
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
            <v-select
                dense
                outlined
                :value="device"
                @input="onInputDevice"
                :disabled="disableDevice && !isEditable"
                :rules="uidRules"
                :items="devices"
                :label="$t('label.uid')"
                item-text="name"
                item-value="uid"
                return-object
            >
              <template v-slot:item="{ item }">
                {{ item.name }}
                <v-chip class="ml-2" x-small outlined color="primary">
                  <v-icon left>mdi-identifier</v-icon>
                  {{ item.uid }}
                </v-chip>
              </template>

              <template v-slot:selection="{ item }">
                {{ item.name }}
                <v-chip class="ml-2" x-small outlined color="primary">
                  <v-icon left>mdi-identifier</v-icon>
                  {{ item.uid }}
                </v-chip>
              </template>
            </v-select>
          </v-list-item>

          <v-list-item>
            <v-text-field
                dense
                outlined
                :disabled="!isEditable"
                :value="author"
                @input="onInputAuthor"
                :label="$t('label.author')"
                :hint="$t('hint.author')"
            ></v-text-field>
          </v-list-item>

          <v-list-item>
            <v-menu
                offset-y
                transition="scale-transition"
                min-width="auto"
                v-model="showTimeMenu"
                :nudge-right="datePickerSize"
                :close-on-content-click="false"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                    dense
                    outlined
                    readonly
                    v-model="time"
                    :disabled="!isEditable"
                    :label="$t('label.time')"
                    :hint="$t('hint.time')"
                    v-bind="attrs"
                    v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                  no-title
                  scrollable
                  :disabled="!isEditable"
                  :value="time"
                  @input="onInputTime"
              ></v-date-picker>
            </v-menu>
          </v-list-item>

          <v-list-item>
            <v-textarea
                dense
                outlined
                :disabled="!isEditable"
                :value="description"
                @input="onInputDescription"
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
          v-if="isEditable"
          :disabled="!modified"
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
import {Component, Prop, Emit, Ref, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {AirjoyDeviceA, AirjoyServiceA} from '@/packet/airjoy';
import {UNKNOWN_AIRJOY_UID} from '@/packet/airjoy';
import {VForm} from 'vuetify/lib/components/VForm';
import requiredField from '@/rules/required';
import {todayString} from '@/chrono/date';
import {splitDateAndTime} from '@/chrono/iso8601';

export interface ServiceInfo {
  uid: number;
  author: string;
  description: string;
  time: string;
}

@Component
export default class AirjoyServiceCard extends VueBase {
  private readonly uidRules = [requiredField];

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean, default: false})
  readonly submitLoading!: boolean;

  @Prop({type: Array, default: () => { return []; }})
  readonly devices!: Array<AirjoyDeviceA>;

  @Prop({type: Boolean, default: false})
  readonly disableDevice!: boolean;

  @Prop({type: Object})
  readonly service!: AirjoyServiceA;

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  @Ref()
  readonly form!: VForm;

  showTimeMenu = false;
  valid = false;

  originalUid = 0;
  originalAuthor = '';
  originalTime = todayString();
  originalDescription = '';

  device?: AirjoyDeviceA = undefined;
  author = '';
  time = todayString();
  description = '';

  created() {
    this.updateForms(this.service);
  }

  @Watch('service')
  onChangeService(newVal: AirjoyServiceA) {
    this.updateForms(newVal);
  }

  updateForms(service?: AirjoyServiceA) {
    const time = service?.time || todayString();

    this.originalUid = service?.airjoy_uid || UNKNOWN_AIRJOY_UID;
    this.originalAuthor = service?.author || '';
    this.originalTime = splitDateAndTime(time)[0];
    this.originalDescription = service?.description || '';

    if (this.originalUid === UNKNOWN_AIRJOY_UID) {
      this.device = undefined;
    } else {
      this.device = this.devices.find(i => i.uid === this.originalUid);
    }
    this.author = this.originalAuthor;
    this.time = this.originalTime;
    this.description = this.originalDescription;
  }

  get isEditable() {
    return this.hasPermissionManagerEdit();
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

  onInputDevice(value) {
    this.device = value;
  }

  onInputAuthor(value) {
    this.author = value;
  }

  onInputTime(value) {
    this.time = value;
    this.showTimeMenu = true;
  }

  onInputDescription(value) {
    this.description = value;
  }

  get modified() {
    if (this.originalAuthor !== this.author) {
      return true;
    } else if (this.originalTime !== this.time) {
      return true;
    }
    return this.originalDescription !== this.description;
  }

  @Emit()
  cancel() {
    this.author = this.originalAuthor;
    this.time = this.originalTime;
    this.description = this.originalDescription;
  }

  @Emit()
  ok() {
    if (typeof this.device === 'undefined') {
      throw TypeError('Airjoy device is not selected.');
    }
    return {
      uid: this.device.uid,
      author: this.author,
      description: this.description,
      time: this.time,
    } as ServiceInfo;
  }
}
</script>
