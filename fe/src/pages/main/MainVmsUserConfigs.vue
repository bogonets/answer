<i18n lang="yaml">
en:
  groups: "Groups"
  settings: "VMS Settings"
  headers:
    sound: "Sound Settings"
  labels:
    beep: "Enable Beep"
    beep_interval: "Beep interval"
    beep_duration: "Beep duration"
  hints:
    beep: "When an event occurs, an alarm sound is played."
    beep_interval: "A cycle of repeated beeps. It is in seconds."
    beep_duration: "Total time for the beep to repeat. It is in seconds."
  suffix:
    seconds: "Seconds"

ko:
  groups: "Groups"
  settings: "VMS Settings"
  headers:
    sound: "소리 설정"
  labels:
    beep: "비프음 활성화"
    beep_interval: "비프음 간격"
    beep_duration: "비프음 재생 시간"
  hints:
    beep: "이벤트가 발생되면 알람음이 재생됩니다."
    beep_interval: "비프음이 반복되는 주기. 초 단위 입니다."
    beep_duration: "비프음이 반복되는 총 시간. 초 단위 입니다."
  suffix:
    seconds: "초"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-divider></v-divider>
    <v-subheader>{{ $t('headers.sound') }}</v-subheader>

    <left-title
        x-small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('labels.beep')"
        :subheader="$t('hints.beep')"
    >
      <div class="d-flex flex-row justify-end">
        <v-switch
            inset
            hide-details
            :disabled="loading"
            v-model="vmsBeep"
            @change="onChangeBeep"
        ></v-switch>
      </div>
    </left-title>

    <left-title
        x-small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('labels.beep_interval')"
        :subheader="$t('hints.beep_interval')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            :disabled="loading"
            :items="intervals"
            :value="vmsBeepInterval"
            @change="onChangeBeepInterval"
            :suffix="$t('suffix.seconds')"
        ></v-combobox>
      </div>
    </left-title>

    <left-title
        x-small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('labels.beep_duration')"
        :subheader="$t('hints.beep_duration')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            :disabled="loading"
            :items="durations"
            :value="vmsBeepDuration"
            @change="onChangeBeepDuration"
            :suffix="$t('suffix.seconds')"
        ></v-combobox>
      </div>
    </left-title>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
  }
})
export default class MainVmsUserConfigs extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly breadcrumbs = [
    {
      text: this.$t('groups'),
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
    },
    {
      text: this.$t('settings'),
      disabled: true,
    },
  ];

  readonly intervals = [
    '2',
    '5',
  ];

  readonly durations = [
    '0',
    '10',
  ];

  loading = false;

  vmsBeep = false;
  vmsBeepInterval = '';
  vmsBeepDuration = '';

  created() {
    const vmsBeep = this.$localStore.userExtra.vmsBeep;
    const vmsBeepInterval = this.$localStore.userExtra.vmsBeepInterval;
    const vmsBeepDuration = this.$localStore.userExtra.vmsBeepDuration;

    this.vmsBeep = !!vmsBeep;

    if (typeof vmsBeepInterval === 'undefined') {
      this.vmsBeepInterval = this.intervals[0];
    } else {
      this.vmsBeepInterval = vmsBeepInterval.toString();
    }

    if (typeof vmsBeepDuration === 'undefined') {
      this.vmsBeepDuration = this.durations[0];
    } else {
      this.vmsBeepDuration = vmsBeepDuration.toString();
    }
  }

  onChangeBeep(value: null | boolean) {
    const extra = this.$localStore.userExtra;
    extra.vmsBeep = !!value;
    this.$localStore.userExtra = extra;
    this.saveUserExtra();
  }

  onChangeBeepInterval(event) {
    const extra = this.$localStore.userExtra;
    let updated = false;
    try {
      extra.vmsBeepInterval = Number.parseInt(event);
      updated = true;
    } catch (error) {
      console.error(error);
    }

    if (updated) {
      this.$localStore.userExtra = extra;
      this.saveUserExtra();
    }
  }

  onChangeBeepDuration(event) {
    const extra = this.$localStore.userExtra;
    let updated = false;
    try {
      extra.vmsBeepDuration = Number.parseInt(event);
      updated = true;
    } catch (error) {
      console.error(error);
    }

    if (updated) {
      this.$localStore.userExtra = extra;
      this.saveUserExtra();
    }
  }

  saveUserExtra(showToast = true) {
    this.loading = true;
    this.$api2.patchSelfExtra(this.$localStore.userExtra)
        .then(() => {
          this.loading = false;
          if (showToast) {
            this.toastRequestSuccess();
          }
        })
        .catch(error => {
          this.loading = false;
          if (showToast) {
            this.toastRequestFailure(error);
          }
        });
  }
}
</script>
