<i18n lang="yaml">
en:
  groups: "Groups"
  settings: "VMS Settings"
  headers:
    common: "Common Settings"
    visual: "Visual Settings"
    sound: "Sound Settings"
  labels:
    popup: "Enable Popup"
    beep: "Enable Beep"
    beep_interval: "Beep interval"
    beep_duration: "Beep duration"
    refresh_interval: "Refresh interval"
  hints:
    popup: "When an event occurs, a popup is output."
    beep: "When an event occurs, an alarm sound is played."
    beep_interval: "A cycle of repeated beeps. It is in seconds."
    beep_duration: "Total time for the beep to repeat. It is in seconds."
    refresh_interval: "You can set the update interval in seconds."
  suffix:
    seconds: "Seconds"

ko:
  groups: "Groups"
  settings: "VMS Settings"
  headers:
    common: "일반 설정"
    visual: "시각 설정"
    sound: "소리 설정"
  labels:
    popup: "팝업 활성화"
    beep: "비프음 활성화"
    beep_interval: "비프음 간격"
    beep_duration: "비프음 재생 시간"
    refresh_interval: "갱신 주기"
  hints:
    popup: "이벤트가 발생하면 팝업이 출력됩니다."
    beep: "이벤트가 발생되면 알람음이 재생됩니다."
    beep_interval: "비프음이 반복되는 주기. 초 단위 입니다."
    beep_duration: "비프음이 반복되는 총 시간. 초 단위 입니다."
    refresh_interval: "갱신 주기를 초 단위로 설정할 수 있습니다."
  suffix:
    seconds: "초"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-subheader>{{ $t('headers.common') }}</v-subheader>

    <left-title
        x-small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('labels.refresh_interval')"
        :subheader="$t('hints.refresh_interval')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            :disabled="loading"
            :items="refreshIntervals"
            :value="vmsRefreshInterval"
            @change="onChangeRefreshInterval"
            :suffix="$t('suffix.seconds')"
        ></v-combobox>
      </div>
    </left-title>

    <v-divider></v-divider>
    <v-subheader>{{ $t('headers.visual') }}</v-subheader>

    <left-title
        x-small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('labels.popup')"
        :subheader="$t('hints.popup')"
    >
      <div class="d-flex flex-row justify-end">
        <v-switch
            inset
            hide-details
            :disabled="loading"
            v-model="vmsPopup"
            @change="onChangePopup"
        ></v-switch>
      </div>
    </left-title>

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
            :items="beepIntervals"
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
import {
  USER_CONFIG_REFRESH_INTERVAL,
  USER_CONFIG_POPUP,
  USER_CONFIG_BEEP,
  USER_CONFIG_BEEP_INTERVAL,
  USER_CONFIG_BEEP_DURATION,
} from "@/packet/vms";

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

  readonly refreshIntervals = [
    '1',
    '2',
    '4',
    '10',
    '30',
    '60',
  ];

  readonly beepIntervals = [
    '2',
    '5',
  ];

  readonly durations = [
    '2',
    '4',
    '6',
    '8',
    '10',
  ];

  loading = false;

  vmsRefreshInterval = '';
  vmsPopup = false;
  vmsBeep = false;
  vmsBeepInterval = '';
  vmsBeepDuration = '';

  created() {
    const extra = this.$localStore.userExtra;
    const refreshInterval = extra.vmsRefreshInterval || USER_CONFIG_REFRESH_INTERVAL;
    const popup = extra.vmsPopup || USER_CONFIG_POPUP;
    const beep = extra.vmsBeep || USER_CONFIG_BEEP;
    const beepInterval = extra.vmsBeepInterval || USER_CONFIG_BEEP_INTERVAL;
    const beepDuration = extra.vmsBeepDuration || USER_CONFIG_BEEP_DURATION;

    this.vmsRefreshInterval = refreshInterval.toString();
    this.vmsPopup = popup;
    this.vmsBeep = beep;
    this.vmsBeepInterval = beepInterval.toString();
    this.vmsBeepDuration = beepDuration.toString();
  }

  onChangeRefreshInterval(event: string) {
    const extra = this.$localStore.userExtra;
    let updated = false;
    try {
      extra.vmsRefreshInterval = Number.parseInt(event);
      updated = true;
    } catch (error) {
      console.error(error);
    }

    if (updated) {
      this.$localStore.userExtra = extra;
      this.saveUserExtra();
    }
  }

  onChangePopup(value: null | boolean) {
    const extra = this.$localStore.userExtra;
    extra.vmsPopup = !!value;
    this.$localStore.userExtra = extra;
    this.saveUserExtra();
  }

  onChangeBeep(value: null | boolean) {
    const extra = this.$localStore.userExtra;
    extra.vmsBeep = !!value;
    this.$localStore.userExtra = extra;
    this.saveUserExtra();
  }

  onChangeBeepInterval(event: string) {
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

  onChangeBeepDuration(event: string) {
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
