<i18n lang="yaml">
en:
  labels:
    device_uid: 'Device UID'
    category: 'Event Category'
    name: 'Name'
    enable: 'Enable'
  hints:
    device_uid: 'The unique ID of the device to which the event will be connected.'
    category: 'Select the event category to apply to the device.'
    name: 'The event name to display on the screen.'
    enable: 'When activated, an event is triggered.'
  category:
    color: 'Color'
    detection: 'Detection'
    matching: 'Matching'
    ocr: 'OCR'
  msg:
    select_category: 'Please select an event category.'
    unknown_category: 'Unknown event category.'
    enable_debugging: 'Enable Device Debugging Mode'
    disable_debugging: 'Disable Device Debugging Mode'
    failed_start_debugging: 'Failed to switch device debugging mode.'
    failed_stop_debugging: 'Failed to stop device debugging mode.'
  step:
    basic: 'Basic'
    event: 'Event'
    confirm: 'Confirm'
  cancel: 'Cancel'
  back: 'Back'
  next: 'Next'
  submit: 'Submit'

ko:
  labels:
    device_uid: 'Device UID'
    category: '이벤트 종류'
    name: '이벤트 이름'
    enable: '활성화'
  hints:
    device_uid: '이벤트가 연결될 장치의 고유한 ID 입니다.'
    category: '장치에 적용할 이벤트의 종류를 선택해 주세요.'
    name: '화면에 표시할 장치 이벤트 입니다.'
    enable: '활성화 되면 이벤트가 작동됩니다.'
  category:
    color: '색상 비교'
    detection: '객체 탐지'
    matching: '영상 비교'
    ocr: '문자 인식'
  msg:
    select_category: '이벤트 종류를 선택해 주세요.'
    unknown_category: '알 수 없는 이벤트 종류 입니다.'
    enable_debugging: '장치 디버깅 모드를 활성화 했습니다.'
    disable_debugging: '장치 디버깅 모드를 비활성화 했습니다.'
    failed_start_debugging: '장치 디버깅 모드 전환에 실패하였습니다.'
    failed_stop_debugging: '장치 디버깅 모드 중단에 실패하였습니다.'
  step:
    basic: '기본 정보'
    event: '이벤트 설정'
    confirm: '설정 확인'
  cancel: '취소'
  back: '이전'
  next: '다음'
  submit: '제출'
</i18n>

<template>
  <v-form ref="form" v-model="valid" lazy-validation>
    <!--    <p :class="subtitleClass">{{ $t('labels.device_uid') }}</p>-->
    <!--    <v-select-->
    <!--        dense-->
    <!--        outlined-->
    <!--        :persistent-hint="!(loading || disableDevice)"-->
    <!--        :hide-details="loading || disableDevice"-->
    <!--        :disabled="loading || disableDevice"-->
    <!--        :rules="ruleDevice"-->
    <!--        v-model="device"-->
    <!--        :items="devices"-->
    <!--        :hint="$t('hints.device_uid')"-->
    <!--        item-text="name"-->
    <!--        item-value="device_uid"-->
    <!--        return-object-->
    <!--    >-->
    <!--      <template v-slot:item="{ item }">-->
    <!--        {{ item.name }}-->
    <!--        <v-chip class="ml-2" x-small outlined color="primary">-->
    <!--          <v-icon left>mdi-identifier</v-icon>-->
    <!--          {{ item.device_uid }}-->
    <!--        </v-chip>-->
    <!--      </template>-->

    <!--      <template v-slot:selection="{ item }">-->
    <!--        {{ item.name }}-->
    <!--        <v-chip class="ml-2" x-small outlined color="primary">-->
    <!--          <v-icon left>mdi-identifier</v-icon>-->
    <!--          {{ item.device_uid }}-->
    <!--        </v-chip>-->
    <!--      </template>-->
    <!--    </v-select>-->

    <label-span class="mt-2" size="subtitle-2" opacity="secondary" weight="bold">
      {{ $t('labels.name') }}
    </label-span>
    <v-text-field
      dense
      persistent-hint
      type="text"
      autocomplete="off"
      :disabled="loading"
      :rules="ruleName"
      :value="value.name"
      @input="onInputName"
      :hint="$t('hints.name')"
    ></v-text-field>

    <v-row class="mt-2" no-gutters>
      <div>
        <label-span class="mt-2" size="subtitle-2" opacity="secondary" weight="bold">
          {{ $t('labels.enable') }}
        </label-span>
        <p class="text-caption text--secondary">{{ $t('hints.enable') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch inset :value="value.enable" @change="onChangeEnable"></v-switch>
      </div>
    </v-row>

    <label-span class="mt-2" size="subtitle-2" opacity="secondary" weight="bold">
      {{ $t('labels.category') }}
    </label-span>
    <v-select
      class="category-z-index"
      dense
      outlined
      :persistent-hint="!(loading || disableCategory)"
      :disabled="loading || disableCategory"
      :rules="ruleCategory"
      :value="value.category"
      @input="onInputCategory"
      :items="categories"
      item-text="text"
      item-value="value"
      :hint="$t('hints.category')"
    >
      <template v-slot:item="{item}">
        <v-icon class="mr-2">{{ item.icon }}</v-icon>
        <label-span size="subtitle-2" opacity="secondary" weight="bold">
          {{ item.text }}
        </label-span>
      </template>

      <template v-slot:selection="{item}">
        <v-icon class="mr-2">{{ item.icon }}</v-icon>
        <label-span size="subtitle-2" opacity="secondary" weight="bold">
          {{ item.text }}
        </label-span>
      </template>
    </v-select>

    <v-sheet class="mt-2 pa-2" outlined rounded>
      <form-vms-event-configs-color
        v-if="isColor"
        :device="device"
        :value="value.extra"
        @input="onInputExtra"
        :valid.sync="validExtra"
      ></form-vms-event-configs-color>
      <form-vms-event-configs-detection
        v-else-if="isDetection"
        :device="device"
        :value="value.extra"
        @input="onInputExtra"
        :valid.sync="validExtra"
      ></form-vms-event-configs-detection>
      <form-vms-event-configs-matching
        v-else-if="isMatching"
        :device="device"
        :value="value.extra"
        @input="onInputExtra"
        :valid.sync="validExtra"
      ></form-vms-event-configs-matching>
      <form-vms-event-configs-ocr
        v-else-if="isOcr"
        :device="device"
        :value="value.extra"
        @input="onInputExtra"
        :valid.sync="validExtra"
      ></form-vms-event-configs-ocr>
      <div v-else-if="isNotSelected" class="pa-2 d-flex flex-row align-center">
        <v-icon large color="warning">mdi-alert-circle</v-icon>
        <label-span class="ml-2" size="subtitle-1" color="warning">
          {{ $t('msg.select_category') }}
        </label-span>
      </div>
      <div v-else class="pa-2 d-flex flex-row align-center">
        <v-icon large color="error">mdi-alert-circle</v-icon>
        <label-span class="ml-2" size="subtitle-1" color="error">
          {{ $t('msg.unknown_category') }}
        </label-span>
      </div>
    </v-sheet>

    <v-row v-if="!hideButtons" class="mt-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn v-if="!hideCancelButton" class="mr-4" color="second" @click="cancel">
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
import requiredField from '@/rules/required';
import {
  EVENT_CATEGORY_NAME_COLOR,
  EVENT_CATEGORY_NAME_DETECTION,
  EVENT_CATEGORY_NAME_MATCHING,
  EVENT_CATEGORY_NAME_OCR,
  EVENT_CATEGORIES,
} from '@/packet/vms';
import type {VmsEventConfigA, VmsDeviceA} from '@/packet/vms';
import LabelSpan from '@/components/LabelSpan.vue';
import FormVmsEventConfigsColor from '@/components/FormVmsEventConfigsColor.vue';
import FormVmsEventConfigsDetection from '@/components/FormVmsEventConfigsDetection.vue';
import FormVmsEventConfigsMatching from '@/components/FormVmsEventConfigsMatching.vue';
import FormVmsEventConfigsOcr from '@/components/FormVmsEventConfigsOcr.vue';

function createEmptyVmsEventConfigA() {
  return {
    // [IMPORTANT]
    // Required for child components.
    extra: {
      // EMPTY.
    },
  } as VmsEventConfigA;
}

@Component({
  components: {
    LabelSpan,
    FormVmsEventConfigsColor,
    FormVmsEventConfigsDetection,
    FormVmsEventConfigsMatching,
    FormVmsEventConfigsOcr,
  },
})
export default class FormVmsEventConfig extends VueBase {
  readonly ruleName = [requiredField];
  readonly ruleCategory = [
    requiredField,
    x => EVENT_CATEGORIES.includes(x) || this.$t('msg.unknown_category'),
  ];

  readonly categories = [
    {
      icon: 'mdi-palette',
      text: this.$t('category.color'),
      value: EVENT_CATEGORY_NAME_COLOR,
    },
    // {
    //   icon: 'mdi-image-search',
    //   text: this.$t('category.detection'),
    //   value: EVENT_CATEGORY_NAME_DETECTION,
    // },
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

  @Prop({type: Object, default: createEmptyVmsEventConfigA})
  readonly value!: VmsEventConfigA;

  @Ref()
  readonly form!: VForm;

  valid = false;
  validExtra = false;
  loading = false;

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

  get isNotSelected() {
    return !this.value.category;
  }

  get disableSubmit() {
    return (
      this.loadingSubmit || !this.valid || !this.validExtra || this.disableSubmitButton
    );
  }

  onInputName(event: string) {
    this.$set(this.value, 'name', event);
    this.input();
  }

  onChangeEnable(event?: boolean | null) {
    this.$set(this.value, 'enable', !!event);
    this.input();
  }

  onInputCategory(event: string) {
    this.$set(this.value, 'category', event);
    this.input();
  }

  onInputExtra(event: any) {
    this.$set(this.value, 'extra', event);
    this.input();
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
  input() {
    return this.value;
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
