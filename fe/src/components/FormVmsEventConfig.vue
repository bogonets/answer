<i18n lang="yaml">
en:
  labels:
    device_uid: "Device UID"
    category: "Event Category"
    name: "Name"
    enable: "Enable"
  hints:
    device_uid: "The unique ID of the device to which the event will be connected."
    category: "Select the event category to apply to the device."
    name: "The event name to display on the screen."
    enable: "When activated, an event is triggered."
  category:
    color: "Color"
    detection: "Detection"
    matching: "Matching"
    ocr: "OCR"
  msg:
    select_category: "Please select an event category."
    unknown_category: "Unknown event category."
    enable_debugging: "Enable Device Debugging Mode"
    disable_debugging: "Disable Device Debugging Mode"
    failed_start_debugging: "Failed to switch device debugging mode."
    failed_stop_debugging: "Failed to stop device debugging mode."
  step:
    basic: "Basic"
    event: "Event"
    confirm: "Confirm"
  cancel: "Cancel"
  back: "Back"
  next: "Next"
  submit: "Submit"

ko:
  labels:
    device_uid: "Device UID"
    category: "이벤트 종류"
    name: "이벤트 이름"
    enable: "활성화"
  hints:
    device_uid: "이벤트가 연결될 장치의 고유한 ID 입니다."
    category: "장치에 적용할 이벤트의 종류를 선택해 주세요."
    name: "화면에 표시할 장치 이벤트 입니다."
    enable: "활성화 되면 이벤트가 작동됩니다."
  category:
    color: "색상 비교"
    detection: "객체 탐지"
    matching: "영상 비교"
    ocr: "문자 인식"
  msg:
    select_category: "이벤트 종류를 선택해 주세요."
    unknown_category: "알 수 없는 이벤트 종류 입니다."
    enable_debugging: "장치 디버깅 모드를 활성화 했습니다."
    disable_debugging: "장치 디버깅 모드를 비활성화 했습니다."
    failed_start_debugging: "장치 디버깅 모드 전환에 실패하였습니다."
    failed_stop_debugging: "장치 디버깅 모드 중단에 실패하였습니다."
  step:
    basic: "기본 정보"
    event: "이벤트 설정"
    confirm: "설정 확인"
  cancel: "취소"
  back: "이전"
  next: "다음"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid" lazy-validation>
    <p :class="subtitleClass">{{ $t('labels.device_uid') }}</p>
    <v-select
        dense
        outlined
        :persistent-hint="!(loading || disableDevice)"
        :hide-details="loading || disableDevice"
        :disabled="loading || disableDevice"
        :rules="ruleDevice"
        v-model="device"
        :items="devices"
        :hint="$t('hints.device_uid')"
        item-text="name"
        item-value="device_uid"
        return-object
    >
      <template v-slot:item="{ item }">
        {{ item.name }}
        <v-chip class="ml-2" x-small outlined color="primary">
          <v-icon left>mdi-identifier</v-icon>
          {{ item.device_uid }}
        </v-chip>
      </template>

      <template v-slot:selection="{ item }">
        {{ item.name }}
        <v-chip class="ml-2" x-small outlined color="primary">
          <v-icon left>mdi-identifier</v-icon>
          {{ item.device_uid }}
        </v-chip>
      </template>
    </v-select>

    <p :class="subtitleClass">{{ $t('labels.name') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="text"
        autocomplete="off"
        :disabled="loading"
        :rules="ruleName"
        v-model="value.name"
        :hint="$t('hints.name')"
    ></v-text-field>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('labels.enable') }}</p>
        <p class="text-caption text--secondary">{{ $t('hints.enable') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch inset v-model="value.enable"></v-switch>
      </div>
    </v-row>

    <p :class="subtitleClass">{{ $t('labels.category') }}</p>
    <v-select
        class="category-z-index"
        dense
        outlined
        :persistent-hint="!(loading || disableCategory)"
        :disabled="loading || disableCategory"
        :rules="ruleCategory"
        v-model="value.category"
        :items="categories"
        item-text="text"
        item-value="value"
        :hint="$t('hints.category')"
    >
      <template v-slot:item="{ item }">
        <v-icon class="mr-2">{{ item.icon }}</v-icon>
        <span :class="subtitleClass">{{ item.text }}</span>
      </template>

      <template v-slot:selection="{ item }">
        <v-icon class="mr-2">{{ item.icon }}</v-icon>
        <span :class="subtitleClass">{{ item.text }}</span>
      </template>
    </v-select>

    <div class="mt-2">
      <v-sheet v-if="existsCategory" class="pa-2" outlined rounded>
        <form-vms-event-configs-color
            v-if="isColor"
            v-model="value.extra"
            :valid.sync="validExtra"
        ></form-vms-event-configs-color>
        <form-vms-event-configs-detection
            v-else-if="isDetection"
            v-model="value.extra"
            :valid.sync="validExtra"
        ></form-vms-event-configs-detection>
        <form-vms-event-configs-matching
            v-else-if="isMatching"
            v-model="value.extra"
            :valid.sync="validExtra"
        ></form-vms-event-configs-matching>
        <form-vms-event-configs-ocr
            v-else-if="isOcr"
            v-model="value.extra"
            :valid.sync="validExtra"
        ></form-vms-event-configs-ocr>
      </v-sheet>
      <div v-else-if="!value.category">
        <v-alert outlined icon="mdi-alert" type="warning">
          {{ $t('msg.select_category') }}
        </v-alert>
      </div>
      <div v-else>
        <v-alert outlined icon="mdi-alert" type="error">
          {{ $t('msg.unknown_category') }}
        </v-alert>
      </div>
    </div>

    <v-row v-if="!hideButtons" class="mt-2" no-gutters>
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
          :loading="loadingSubmit"
          :disabled="disableSubmit"
          @click="onSubmit"
      >
        {{ $t('submit') }}
      </v-btn>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import {Component, Emit, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import requiredField from '@/rules/required';
import {
  EVENT_CATEGORIES,
  EVENT_CATEGORY_NAME_COLOR,
  EVENT_CATEGORY_NAME_DETECTION,
  EVENT_CATEGORY_NAME_MATCHING,
  EVENT_CATEGORY_NAME_OCR,
} from '@/packet/vms';
import type {
  VmsDeviceA,
  VmsEventConfigA,
} from '@/packet/vms';
import FormVmsEventConfigsColor from "@/components/FormVmsEventConfigsColor.vue";
import FormVmsEventConfigsDetection from "@/components/FormVmsEventConfigsDetection.vue";
import FormVmsEventConfigsMatching from "@/components/FormVmsEventConfigsMatching.vue";
import FormVmsEventConfigsOcr from "@/components/FormVmsEventConfigsOcr.vue";

@Component({
  components: {
    FormVmsEventConfigsColor,
    FormVmsEventConfigsDetection,
    FormVmsEventConfigsMatching,
    FormVmsEventConfigsOcr,
  },
})
export default class FormVmsEventConfig extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly ruleDevice = [requiredField];
  readonly ruleCategory = [requiredField];
  readonly ruleName = [requiredField];

  readonly categories = [
    {
      icon: 'mdi-palette',
      text: this.$t('category.color'),
      value: EVENT_CATEGORY_NAME_COLOR,
    },
    {
      icon: 'mdi-image-search',
      text: this.$t('category.detection'),
      value: EVENT_CATEGORY_NAME_DETECTION,
    },
    {
      icon: 'mdi-compare',
      text: this.$t('category.matching'),
      value: EVENT_CATEGORY_NAME_MATCHING,
    },
    {
      icon: 'mdi-ocr',
      text: this.$t('category.ocr'),
      value: EVENT_CATEGORY_NAME_OCR,
    },
  ];

  @Prop({type: Boolean})
  readonly disableDevice!: boolean;

  @Prop({type: Boolean})
  readonly disableCategory!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly loadingSubmit!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Object, default: () => new Object()})
  readonly device!: VmsDeviceA;

  @Prop({type: Array, default: () => []})
  readonly devices!: Array<VmsDeviceA>;

  @Prop({type: Object, default: () => new Object()})
  readonly value!: VmsEventConfigA;

  @Ref()
  readonly form!: VForm;

  valid = false;
  validExtra = false;
  loading = false;

  // // You cannot directly reference `$route` in the `beforeDestroy` event.
  // currentGroup = '';
  // currentProject = '';
  // currentDevice = '';

  get existsCategory() {
    return EVENT_CATEGORIES.includes(this.value.category);
  }

  get isColor() {
    return this.value.category === EVENT_CATEGORY_NAME_COLOR;
  }

  get isDetection() {
    return this.value.category === EVENT_CATEGORY_NAME_DETECTION;
  }

  get isMatching() {
    return this.value.category === EVENT_CATEGORY_NAME_MATCHING;
  }

  get isOcr() {
    return this.value.category === EVENT_CATEGORY_NAME_OCR;
  }

  get disableSubmit() {
    return this.loadingSubmit
        || !this.valid
        || !this.validExtra
        || this.disableSubmitButton;
  }

  formValidate() {
    this.form['validate']();
  }

  onSubmit() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid || !this.validExtra) {
        return;
      }
    }

    this.ok();
  }

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit()
  ok() {
    return this.value;
  }
}
</script>

<style lang="scss" scoped>
.category-z-index {
  // The z-index for the v-select-list displayed at the top of the `MediaPlayer`.
  // Media players use a z-index between 0 and 100.
  z-index: 100;
}
</style>
