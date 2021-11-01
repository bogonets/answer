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
  <v-card>
    <v-card-title class="mb-1">{{ title }}</v-card-title>
    <v-card-subtitle>{{ subtitle }}</v-card-subtitle>
    <v-divider></v-divider>

    <v-stepper elevation="0" v-model="step">
      <v-stepper-header>
        <v-stepper-step :complete="step > 1" step="1">
          {{ $t('step.basic') }}
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step :complete="step > 2" step="2">
          {{ $t('step.event') }}
        </v-stepper-step>

        <v-divider></v-divider>

        <v-stepper-step step="3">
          {{ $t('step.confirm') }}
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <v-form ref="form" v-model="valid" lazy-validation>
            <p :class="subtitleClass">{{ $t('labels.device_uid') }}</p>
            <v-select
                dense
                outlined
                :persistent-hint="!(loading || disableDevice)"
                :hide-details="loading || disableDevice"
                :disabled="loading || disableDevice"
                :rules="ruleDevice"
                :value="device"
                @input="inputDevice"
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

            <p :class="subtitleClass">{{ $t('labels.category') }}</p>
            <v-select
                dense
                outlined
                :persistent-hint="!(loading || disableCategory)"
                :disabled="loading || disableCategory"
                :rules="ruleCategory"
                :value="value.category"
                @input="inputCategory"
                :items="categories"
                item-text="text"
                item-value="value"
                :hint="$t('hints.category')"
            >
              <template v-slot:item="{ item }">
                <v-icon class="mr-2">{{ item.icon }}</v-icon>
                <span :class="subtitleClass">
                  {{ item.text }}
                </span>
              </template>

              <template v-slot:selection="{ item }">
                <v-icon class="mr-2">{{ item.icon }}</v-icon>
                <span :class="subtitleClass">
                  {{ item.text }}
                </span>
              </template>
            </v-select>
          </v-form>

          <v-row class="mt-4 mb-2" no-gutters>
            <v-spacer></v-spacer>
            <v-btn class="mr-4" color="second" @click="cancel">
              {{ $t('cancel') }}
            </v-btn>
            <v-btn color="primary" @click="onClickNext">
              {{ $t('next') }}
            </v-btn>
          </v-row>
        </v-stepper-content>

        <v-stepper-content step="2">
          <v-sheet v-if="existsCategory" class="pa-2" outlined rounded>
            <form-vms-event-configs-color
                v-if="isColor"
                :value="value.extra"
                @input="inputExtra"
            ></form-vms-event-configs-color>
            <form-vms-event-configs-detection
                v-else-if="isDetection"
                :value="value.extra"
                @input="inputExtra"
            ></form-vms-event-configs-detection>
            <form-vms-event-configs-matching
                v-else-if="isMatching"
                :value="value.extra"
                @input="inputExtra"
            ></form-vms-event-configs-matching>
            <form-vms-event-configs-ocr
                v-else-if="isOcr"
                :value="value.extra"
                @input="inputExtra"
            ></form-vms-event-configs-ocr>
          </v-sheet>
          <div v-else-if="!value.category">
            <v-alert dense outlined type="warning">
              {{ $t('msg.select_category') }}
            </v-alert>
          </div>
          <div v-else>
            <v-alert dense outlined type="error">
              {{ $t('msg.unknown_category') }}
            </v-alert>
          </div>

          <v-row class="mt-4 mb-2" no-gutters>
            <v-spacer></v-spacer>
            <v-btn class="mr-4" color="second" @click="onClickBack">
              {{ $t('back') }}
            </v-btn>
            <v-btn color="primary" @click="onClickNext">
              {{ $t('next') }}
            </v-btn>
          </v-row>
        </v-stepper-content>

        <v-stepper-content step="3">
          <p :class="subtitleClass">{{ $t('labels.name') }}</p>
          <v-text-field
              dense
              persistent-hint
              type="text"
              autocomplete="off"
              :disabled="loading"
              :rules="ruleName"
              :value="value.name"
              @input="inputName"
              :hint="$t('hints.name')"
          ></v-text-field>

          <v-row class="mt-2" no-gutters>
            <div>
              <p :class="subtitleClass">{{ $t('labels.enable') }}</p>
              <p class="text-caption text--secondary">{{ $t('hints.enable') }}</p>
            </div>
            <v-spacer></v-spacer>
            <div>
              <v-switch
                  inset
                  :value="value.enable"
                  @change="onChangeEnable"
              ></v-switch>
            </div>
          </v-row>

          <v-row class="mt-4 mb-2" no-gutters>
            <v-spacer></v-spacer>
            <v-btn class="mr-4" color="second" @click="onClickBack">
              {{ $t('back') }}
            </v-btn>
            <v-btn color="primary" @click="ok">
              {{ $t('submit') }}
            </v-btn>
          </v-row>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>

<!--    <v-row v-if="!hideButtons" class="mt-4 mb-2" no-gutters>-->
<!--      <v-spacer></v-spacer>-->
<!--      <v-btn-->
<!--          v-if="!hideCancelButton"-->
<!--          class="mr-4"-->
<!--          color="second"-->
<!--          @click="cancel"-->
<!--      >-->
<!--        {{ $t('cancel') }}-->
<!--      </v-btn>-->
<!--      <v-btn-->
<!--          v-if="!hideSubmitButton"-->
<!--          color="primary"-->
<!--          :loading="loading"-->
<!--          :disabled="disableSubmit"-->
<!--          @click="onSubmit"-->
<!--      >-->
<!--        {{ $t('submit') }}-->
<!--      </v-btn>-->
<!--    </v-row>-->

  </v-card>
</template>

<script lang="ts">
import {Component, Prop, Emit, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import FormVmsEventConfigsColor from '@/components/FormVmsEventConfigsColor.vue';
import FormVmsEventConfigsDetection from '@/components/FormVmsEventConfigsDetection.vue';
import FormVmsEventConfigsMatching from '@/components/FormVmsEventConfigsMatching.vue';
import FormVmsEventConfigsOcr from '@/components/FormVmsEventConfigsOcr.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import requiredField from '@/rules/required';
import type {
  VmsDeviceA,
  VmsEventConfigA,
  VmsCreateEventConfigQ,
} from '@/packet/vms';
import {
  createEmptyVmsEventConfigA,
  EVENT_CATEGORY_NAME_COLOR,
  EVENT_CATEGORY_NAME_DETECTION,
  EVENT_CATEGORY_NAME_MATCHING,
  EVENT_CATEGORY_NAME_OCR,
  EVENT_CATEGORIES,
} from '@/packet/vms';
import * as _ from 'lodash';

@Component({
  components: {
    FormVmsEventConfigsColor,
    FormVmsEventConfigsDetection,
    FormVmsEventConfigsMatching,
    FormVmsEventConfigsOcr,
  },
})
export default class CardInfoNew extends VueBase {
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

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean})
  readonly disableDevice!: boolean;

  @Prop({type: Boolean})
  readonly disableCategory!: boolean;

  @Prop({type: Object, default: createEmptyVmsEventConfigA})
  readonly value!: VmsEventConfigA;

  @Prop({type: Boolean})
  readonly disableSubmit!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Ref()
  readonly form!: VForm;

  valid = false;
  loading = false;
  init = false;

  // You cannot directly reference `$route` in the `beforeDestroy` event.
  debuggingGroup = '';
  debuggingProject = '';
  debuggingDevice = '';

  device = {} as VmsDeviceA;
  devices = [] as Array<VmsDeviceA>;

  step = 1;

  created() {
    this.requestSetup();
  }

  requestSetup() {
    this.loading = true;
    this.init = false;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    try {
      this.devices = await this.$api2.getVmsDevices(group, project);

      const device_uid = Number.parseInt(device);
      const findDevice = this.devices.find(i => i.device_uid == device_uid);
      if (typeof findDevice === 'undefined') {
        this.device = {} as VmsDeviceA;
      } else {
        this.device = findDevice;
      }

      // this.original = _.cloneDeep(vmsLayout);
      // this.current = _.cloneDeep(vmsLayout);
      // this.modified = false;

      this.init = true;
    } catch (error) {
      this.toastRequestFailure(error);
      this.init = false;
    }

    try {
      if (this.init) {
        await this.$api2.postVmsDeviceProcessDebugStart(group, project, device);
        this.debuggingGroup = this.$route.params.group;
        this.debuggingProject = this.$route.params.project;
        this.debuggingDevice = this.$route.params.device;

        this.toastInfo(this.$t('msg.enable_debugging'));
      }
    } catch (error) {
      this.toastWarning(this.$t('msg.failed_start_debugging'));
    } finally {
      this.loading = false;
    }
  }

  beforeDestroy() {
    const group = this.debuggingGroup;
    const project = this.debuggingProject;
    const device = this.debuggingDevice;
    this.$api2.postVmsDeviceProcessDebugStop(group, project, device)
        .then(() => {
          this.toastSuccess(this.$t('msg.disable_debugging'));
        })
        .catch(() => {
          this.toastWarning(this.$t('msg.failed_stop_debugging'));
        });
  }

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

  inputDevice(value: VmsDeviceA) {
    this.device = value;
    this.value.device_uid = value.device_uid;
    this.input();
  }

  inputCategory(event: string) {
    this.value.category = event;
    this.input();
  }

  inputName(event: string) {
    this.value.name = event;
    this.input();
  }

  inputExtra(event) {
    this.value.extra = event;
    this.input();
  }

  onChangeEnable(event: null | boolean) {
    this.value.enable = !!event;
    this.input();
  }

  onClickBack() {
    this.step -= 1;
  }

  onClickNext() {
    this.step += 1;
  }

  @Emit()
  input() {
    return this.value;
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
  cancel() {
  }

  @Emit()
  ok() {
    return {
      sequence: 0,
      device_uid: Number.parseInt(this.debuggingDevice),
      category: this.value.category,
      name: this.value.name,
      enable: this.value.enable,
      extra: this.value.extra,
    } as VmsCreateEventConfigQ;
  }
}
</script>
