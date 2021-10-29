<i18n lang="yaml">
en:
  msg:
    unknown_event_type: ""

ko:
  msg:
    unknown_event_type: ""
</i18n>

<template>
  <v-card>
    <v-card-title class="mb-1">{{ title }}</v-card-title>
    <v-card-subtitle>{{ subtitle }}</v-card-subtitle>
    <v-divider></v-divider>

    <div>
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
      <div v-else>
        <span>
          {{ $t('msg.unknown_event_type') }}
        </span>
      </div>
    </div>

  </v-card>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import FormVmsEventConfigsColor from '@/components/FormVmsEventConfigsColor.vue';
import FormVmsEventConfigsDetection from '@/components/FormVmsEventConfigsDetection.vue';
import FormVmsEventConfigsMatching from '@/components/FormVmsEventConfigsMatching.vue';
import FormVmsEventConfigsOcr from '@/components/FormVmsEventConfigsOcr.vue';
import type {VmsEventConfigA} from '@/packet/vms';
import {
  createEmptyVmsEventConfigA,
  EVENT_TYPE_NAME_COLOR,
  EVENT_TYPE_NAME_DETECTION,
  EVENT_TYPE_NAME_MATCHING,
  EVENT_TYPE_NAME_OCR,
} from '@/packet/vms';

@Component({
  components: {
    FormVmsEventConfigsColor,
    FormVmsEventConfigsDetection,
    FormVmsEventConfigsMatching,
    FormVmsEventConfigsOcr,
  },
})
export default class CardInfoNew extends VueBase {
  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Object, default: createEmptyVmsEventConfigA})
  readonly value!: VmsEventConfigA;

  get isColor() {
    return this.value.type === EVENT_TYPE_NAME_COLOR;
  }

  get isDetection() {
    return this.value.type === EVENT_TYPE_NAME_DETECTION;
  }

  get isMatching() {
    return this.value.type === EVENT_TYPE_NAME_MATCHING;
  }

  get isOcr() {
    return this.value.type === EVENT_TYPE_NAME_OCR;
  }

  inputExtra(event) {
    this.value.extra = event;
    this.input();
  }

  @Emit()
  input() {
    return this.value;
  }
}
</script>
