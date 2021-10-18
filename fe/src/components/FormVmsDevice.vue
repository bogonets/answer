<i18n lang="yaml">
en:
  cancel: "Cancel"
  submit: "Submit"
  labels:
    device_uid: "Device UID"
    name: "Name"
    description: "Description"
    stream_address: "Stream Address"
    onvif_address: "ONVIF Address"
    server_address: "Server Address"
    username: "Username"
    password: "Password"
    protocol: "Transport Protocol"
    stream: "Stream Type"
    active: "Active"
    daemon: "Daemon"
  hints:
    device_uid: "This is a number that identifies the device."
    name: "The name of the device as it appears on the screen."
    description: "A specific description of the device."
    stream_address: "Media streaming address."
    onvif_address: "ONVIF Device Manager address."
    server_address: "Internal server address for media streaming."
    username: "This is the username for accessing media streaming."
    password: "This is the password for accessing media streaming."
    active: "When enabled, all features are activate."
    daemon: "When enabled, it works as a service."

ko:
  cancel: "취소"
  submit: "제출"
  labels:
    device_uid: "장치 UID"
    name: "이름"
    description: "설명"
    stream_address: "스트림 주소"
    onvif_address: "ONVIF 주소"
    server_address: "내부 서버 주소"
    username: "사용자명"
    password: "비밀번호"
    protocol: "전송 프로토콜"
    stream: "스트림 유형"
    active: "Active"
    daemon: "Daemon"
  hints:
    device_uid: "장치를 식별할 수 있는 번호 입니다."
    name: "화면에 표시되는 장치의 이름입니다."
    description: "장치의 구체적인 설명."
    stream_address: "미디어 스트리밍 주소 입니다."
    onvif_address: "ONVIF 장치 관리 주소 입니다."
    server_address: "미디어 스트리밍을 위한 내부 서버 주소 입니다."
    username: "미디어 스트리밍 접속을 위한 사용자 이름 입니다."
    password: "미디어 스트리밍 접속을 위한 비밀번호 입니다."
    active: "활성화 되면, 모든 기능을 사용합니다."
    daemon: "활성화 되면, 서비스로 작동합니다."
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <p v-if="showDeviceUid" :class="subtitleClass">{{ $t('labels.device_uid') }}</p>
    <v-text-field
        v-if="showDeviceUid"
        dense
        disabled
        filled
        persistent-hint
        :value="value.device_uid"
        @input="onInputDeviceUid"
        :hint="$t('hints.device_uid')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.name') }}</p>
    <v-text-field
        dense
        persistent-hint
        :value="value.name"
        @input="onInputName"
        :hint="$t('hints.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.description') }}</p>
    <v-textarea
        dense
        auto-grow
        persistent-hint
        :value="value.description"
        @input="onInputDescription"
        :hint="$t('hints.description')"
    ></v-textarea>

    <p :class="subtitleClass">{{ $t('labels.stream_address') }}</p>
    <v-text-field
        dense
        persistent-hint
        :value="value.stream_address"
        @input="onInputStreamAddress"
        :hint="$t('hints.stream_address')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.onvif_address') }}</p>
    <v-text-field
        dense
        persistent-hint
        :value="value.onvif_address"
        @input="onInputOnvifAddress"
        :hint="$t('hints.onvif_address')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.server_address') }}</p>
    <v-text-field
        dense
        persistent-hint
        :value="value.server_address"
        @input="onInputServerAddress"
        :hint="$t('hints.server_address')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.username') }}</p>
    <v-text-field
        dense
        persistent-hint
        :value="value.username"
        @input="onInputUsername"
        :hint="$t('hints.username')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.password') }}</p>
    <v-text-field
        dense
        persistent-hint
        :type="showPassword ? 'text' : 'password'"
        :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
        :value="value.password"
        @input="onInputPassword"
        :hint="$t('hints.password')"
        @click:append="showPassword = !showPassword"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.stream') }}</p>
    <v-radio-group
        class="mt-2"
        row
        hide-details
        :value="value.stream"
        @change="onChangeStream"
    >
      <v-radio
          v-for="stream in streamTypes"
          :key="stream"
          :label="stream"
          :value="stream"
      ></v-radio>
    </v-radio-group>

    <p :class="subtitleClass">{{ $t('labels.protocol') }}</p>
    <v-radio-group
        class="mt-2"
        row
        hide-details
        :value="value.protocol"
        @change="onChangeProtocol"
    >
      <v-radio
          v-for="proto in protocols"
          :key="proto"
          :label="proto"
          :value="proto"
      ></v-radio>
    </v-radio-group>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('labels.active') }}</p>
        <p class="text-caption text--secondary">{{ $t('hints.active') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
            inset
            :value="value.active"
            @change="onChangeActive"
        ></v-switch>
      </div>
    </v-row>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('labels.daemon') }}</p>
        <p class="text-caption text--secondary">{{ $t('hints.daemon') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
            inset
            :value="value.daemon"
            @change="onChangeDaemon"
        ></v-switch>
      </div>
    </v-row>

    <v-row v-if="!hideButtons" class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          v-if="!hideCancelButton"
          class="mr-4"
          color="second"
          @click="cancel"
      >
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
          v-if="!hideSubmitButton"
          color="primary"
          :loading="loading"
          :disabled="disableSubmit"
          @click="onSubmit"
      >
        {{ $t('submit') }}
      </v-btn>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Emit, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import type {VmsDeviceA} from '@/packet/vms';
import {PROTOCOLS, STREAM_TYPES, createEmptyVmsDeviceA} from '@/packet/vms';

@Component
export default class FormVmsDevice extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;

  readonly streamTypes = STREAM_TYPES;
  readonly protocols = PROTOCOLS;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly showDeviceUid!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Object, default: createEmptyVmsDeviceA})
  readonly value!: VmsDeviceA;

  @Ref()
  readonly form!: VForm;

  valid = false;
  showPassword = false;

  onInputDeviceUid(event: number) {
    this.value.device_uid = event;
    this.input();
  }

  onInputName(event: string) {
    this.value.name = event;
    this.input();
  }

  onInputDescription(event: string) {
    this.value.description = event;
    this.input();
  }

  onInputStreamAddress(event: string) {
    this.value.stream_address = event;
    this.input();
  }

  onInputOnvifAddress(event: string) {
    this.value.onvif_address = event;
    this.input();
  }

  onInputServerAddress(event: string) {
    this.value.server_address = event;
    this.input();
  }

  onInputUsername(event: string) {
    this.value.username = event;
    this.input();
  }

  onInputPassword(event: string) {
    this.value.password = event;
    this.input();
  }

  onChangeStream(event: string) {
    this.value.stream = event;
    this.input();
  }

  onChangeProtocol(event: string) {
    this.value.protocol = event;
    this.input();
  }

  onChangeActive(event: null | boolean) {
    this.value.active = !!event;
    this.input();
  }

  onChangeDaemon(event: null | boolean) {
    this.value.daemon = !!event;
    this.input();
  }

  get disableSubmit(): boolean {
    return this.loading || !this.valid || this.disableSubmitButton;
  }

  formValidate() {
    this.form['validate']();
  }

  onSubmit() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.ok();
  }

  @Emit()
  input() {
    return this.value;
  }

  @Emit()
  cancel() {
    return this.value;
  }

  @Emit()
  ok() {
    return this.value;
  }
}
</script>
