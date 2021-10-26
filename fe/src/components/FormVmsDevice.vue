<i18n lang="yaml">
en:
  cancel: "Cancel"
  submit: "Submit"
  delete: "Delete"
  labels:
    device_uid: "Device UID"
    name: "Name"
    description: "Description"
    stream_address: "Stream Address"
    onvif_address: "ONVIF Address"
    server_address: "Server Address"
    ai_address: "AI Address"
    ices: "ICE Servers"
    add: "Add"
    username: "Username"
    password: "Password"
    protocol: "Transport Protocol"
    stream: "Stream Type"
    active: "Active"
    daemon: "Daemon"
    delete: "Delete a device"
  hints:
    device_uid: "This is a number that identifies the device."
    name: "The name of the device as it appears on the screen."
    description: "A specific description of the device."
    stream_address: "Media streaming address."
    onvif_address: "ONVIF Device Manager address."
    server_address: "Internal server address for media streaming."
    ai_address: "Server address providing AI services."
    ices: "STUN or TURN servers."
    username: "This is the username for accessing media streaming."
    password: "This is the password for accessing media streaming."
    active: "When enabled, all features are activate."
    daemon: "When enabled, it works as a service."
    delete: "Please be careful! It cannot be recovered."
  msg:
    delete_confirm: "Are you sure? Are you really removing this device?"
    empty_ices: >
      There is no registered ICE server.
      Please add it in the same format as {stun}.

ko:
  cancel: "취소"
  submit: "제출"
  delete: "제거"
  labels:
    device_uid: "장치 UID"
    name: "이름"
    description: "설명"
    stream_address: "스트림 주소"
    onvif_address: "ONVIF 주소"
    server_address: "내부 서버 주소"
    ai_address: "인공지능 서버 주소"
    ices: "ICE 서버 목록"
    add: "추가"
    username: "사용자명"
    password: "비밀번호"
    protocol: "전송 프로토콜"
    stream: "스트림 유형"
    active: "활성화"
    daemon: "데몬"
    delete: "장치 제거"
  hints:
    device_uid: "장치를 식별할 수 있는 번호 입니다."
    name: "화면에 표시되는 장치의 이름입니다."
    description: "장치의 구체적인 설명."
    stream_address: "미디어 스트리밍 주소 입니다."
    onvif_address: "ONVIF 장치 관리 주소 입니다."
    server_address: "미디어 스트리밍을 위한 내부 서버 주소 입니다."
    ai_address: "AI 서비스를 제공하는 서버 주소입니다."
    ices: "STUN 또는 TURN 서버."
    username: "미디어 스트리밍 접속을 위한 사용자 이름 입니다."
    password: "미디어 스트리밍 접속을 위한 비밀번호 입니다."
    active: "활성화 되면, 모든 기능을 사용합니다."
    daemon: "활성화 되면, 서비스로 작동합니다."
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  msg:
    delete_confirm: "이 장치를 정말 제거합니까?"
    empty_ices: >
      등록된 ICE 서버가 없습니다.
      {stun} 와 같은 형식으로 추가해 주세요.
</i18n>

<template>
  <div>
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
          :disabled="disabled"
          :value="value.name"
          @input="onInputName"
          :hint="$t('hints.name')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('labels.description') }}</p>
      <v-textarea
          dense
          auto-grow
          persistent-hint
          rows="1"
          :disabled="disabled"
          :value="value.description"
          @input="onInputDescription"
          :hint="$t('hints.description')"
      ></v-textarea>

      <p :class="subtitleClass">{{ $t('labels.stream_address') }}</p>
      <v-text-field
          dense
          persistent-hint
          :disabled="disabled"
          :value="value.stream_address"
          @input="onInputStreamAddress"
          :hint="$t('hints.stream_address')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('labels.onvif_address') }}</p>
      <v-text-field
          dense
          persistent-hint
          :disabled="disabled"
          :value="value.onvif_address"
          @input="onInputOnvifAddress"
          :hint="$t('hints.onvif_address')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('labels.server_address') }}</p>
      <v-text-field
          dense
          persistent-hint
          :disabled="disabled"
          :value="value.server_address"
          @input="onInputServerAddress"
          :hint="$t('hints.server_address')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('labels.ai_address') }}</p>
      <v-text-field
          dense
          persistent-hint
          :disabled="disabled"
          :value="value.ai_address"
          @input="onInputAiAddress"
          :hint="$t('hints.ai_address')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('labels.ices') }}</p>
      <v-sheet outlined>
        <i18n
            v-if="ices.length === 0"
            :class="captionClass"
            path="msg.empty_ices"
            tag="span"
        >
          <template #stun>
            <code>stun:localhost:3478</code>
          </template>
        </i18n>
        <v-text-field
            v-for="index in ices.length"
            :key="index"
            class="ma-2"
            dense
            hide-details
            append-outer-icon="mdi-minus"
            :disabled="disabled"
            :value="ices[index-1]"
            @input="onInputIce(index, $event)"
            @click:append-outer="onClickIceRemove(index)"
        ></v-text-field>

        <v-row no-gutters>
          <v-spacer></v-spacer>
          <v-btn class="ma-2" small @click="onClickIceAdd">
            <v-icon left>mdi-plus</v-icon>
            {{ $t('labels.add') }}
          </v-btn>
        </v-row>
      </v-sheet>

      <p :class="subtitleClass">{{ $t('labels.username') }}</p>
      <v-text-field
          dense
          persistent-hint
          :disabled="disabled"
          :value="value.username"
          @input="onInputUsername"
          :hint="$t('hints.username')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('labels.password') }}</p>
      <v-text-field
          dense
          persistent-hint
          autocomplete="off"
          :disabled="disabled"
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
          :disabled="disabled"
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
          :disabled="disabled"
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
              :disabled="disabled"
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
              :disabled="disabled"
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

    <v-alert class="mt-6" outlined prominent type="error">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('labels.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hints.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('labels.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('msg.delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script lang="ts">
import {Component, Prop, Watch, Emit, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';
import type {VmsDeviceA} from '@/packet/vms';
import {PROTOCOLS, STREAM_TYPES, createEmptyVmsDeviceA} from '@/packet/vms';

@Component
export default class FormVmsDevice extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  readonly streamTypes = STREAM_TYPES;
  readonly protocols = PROTOCOLS;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly showDeviceUid!: boolean;

  @Prop({type: Boolean})
  readonly disabled!: boolean;

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

  @Prop({type: Boolean})
  readonly showDeleteDialog!: boolean;

  @Prop({type: Boolean})
  readonly loadingDelete!: boolean;

  @Prop({type: Object, default: createEmptyVmsDeviceA})
  readonly value!: VmsDeviceA;

  @Ref()
  readonly form!: VForm;

  valid = false;
  ices = [] as Array<string>;
  showPassword = false;

  created() {
    this.updateIces(this.value.ices);
  }

  updateIces(source?: Array<string>) {
    const result = [] as Array<string>;
    if (typeof source !== 'undefined') {
      if (source) {
        for (const item of source) {
          result.push(item);
        }
      }
    }
    this.ices = result;
  }

  @Watch('value.ices')
  onWatchValueIces(newVal, oldVal) {
    this.updateIces(newVal);
  }

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

  onInputAiAddress(event: string) {
    this.value.ai_address = event;
    this.input();
  }

  onInputIce(index: number, event: string) {
    const arrayIndex = index - 1;
    this.ices[arrayIndex] = event;
    this.value.ices[arrayIndex] = event;
    this.input();
  }

  onClickIceRemove(index: number) {
    const arrayIndex = index - 1;
    this.ices.splice(arrayIndex, 1);
    this.value.ices.splice(arrayIndex, 1);
    this.input();
  }

  onClickIceAdd() {
    this.ices.push('');
    this.value.ices.push('');
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

  @Emit('delete:show')
  onClickDelete() {
    // EMPTY
  }

  @Emit('delete:cancel')
  onClickDeleteCancel() {
    // EMPTY
  }

  @Emit('delete:ok')
  onClickDeleteOk() {
    // EMPTY
  }
}
</script>
