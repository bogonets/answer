<i18n lang="yaml">
en:
  title:
    suffix: 'Air quality monitoring'
    selectDialog: 'Select a device'
  subtitle:
    selectDialog: 'Please select a device ID to output'
  msg:
    selectDevice: 'Please select a device'
  format:
    date: 'ddd, LL'
    time: 'LT'
  categories:
    pm10: 'PM10'
    pm2_5: 'PM2.5'
    co2: 'CO2'
    humidity: 'Humidity'
    temperature: 'Temperature'
    voc: 'VOC'
  values:
    pm10: '{0} μg/m³'
    pm2_5: '{0} μg/m³'
    co2: '{0} ppm'
    humidity: '{0} %'
    temperature: '{0} °C'
    voc: '{0} level'
  state:
    good: 'Good'
    normal: 'Normal'
    warning: 'Warning'
    danger: 'Danger'
    unknown: 'Unknown'
  fullscreen: 'Fullscreen'
  cancel: 'Cancel'
  ok: 'Ok'

ko:
  title:
    suffix: '공기질 모니터링'
    selectDialog: '장치 선택'
  subtitle:
    selectDialog: '출력할 장치 ID를 선택하세요'
  msg:
    selectDevice: '장치를 선택해 주세요'
  format:
    date: 'LL (ddd)'
    time: 'hh:mm A'
  categories:
    pm10: '미세먼지'
    pm2_5: '초미세먼지'
    co2: '이산화탄소'
    humidity: '습도'
    temperature: '온도'
    voc: '유해가스'
  values:
    pm10: '{0} μg/m³'
    pm2_5: '{0} μg/m³'
    co2: '{0} ppm'
    humidity: '{0} %'
    temperature: '{0} °C'
    voc: '{0} level'
  state:
    good: '좋음'
    normal: '보통'
    warning: '나쁨'
    danger: '매우나쁨'
    unknown: '알수없음'
  fullscreen: '전체 화면'
  cancel: '취소'
  ok: '확인'
</i18n>

<template>
  <div>
    <div class="control-panel">
      <video ref="video-player" class="video-player" loop="loop" autoplay muted></video>

      <div class="mt-10 d-flex flex-row align-center justify-center">
        <v-img
          v-if="this.$vuetify.theme.dark"
          src="@/assets/logos/answer-logo-onlytext-dark.svg"
          alt="ANSWER"
          :max-width="logoMinWidth"
          :max-height="logoMinHeight"
        ></v-img>
        <v-img
          v-else
          src="@/assets/logos/answer-logo-onlytext-light.svg"
          alt="ANSWER"
          :max-width="logoMinWidth"
          :max-height="logoMinHeight"
        ></v-img>
        <span class="ml-2 text--primary text-h5">{{ $t('title.suffix') }}</span>
      </div>

      <div class="mt-4 d-flex flex-row align-center justify-center">
        <span class="ml-2 text--primary text-h3">
          {{ deviceName }}
        </span>
      </div>

      <v-container>
        <v-row class="my-8">
          <v-col cols="6">
            <div class="d-flex flex-column align-center justify-center">
              <span class="date-text">{{ nowDate }}</span>
              <span class="time-text">{{ nowTime }}</span>
            </div>
          </v-col>

          <v-col cols="3" class="d-flex flex-column align-center justify-center">
            <div class="d-flex flex-row align-center">
              <v-icon left size="48" :color="iconColor">mdi-thermometer</v-icon>
              <span class="text--primary text-h5">
                {{ $t('categories.temperature') }}
              </span>
            </div>

            <span class="text--primary text-h4 text-no-wrap">
              {{ $t('values.temperature', [calcTemperature(device.temperature)]) }}
            </span>
          </v-col>

          <v-col cols="3" class="d-flex flex-column align-center justify-center">
            <div class="d-flex flex-row align-center">
              <v-icon left size="48" :color="iconColor">mdi-water-outline</v-icon>
              <span class="text--primary text-h5">
                {{ $t('categories.humidity') }}
              </span>
            </div>

            <span class="text--primary text-h4 text-no-wrap">
              {{ $t('values.humidity', [calcHumidityText(device.humidity)]) }}
            </span>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="6">
            <div :class="`card  ${stateClassPm10}`">
              <div class="card--body">
                <span>{{ stateNamePm10 }}</span>
              </div>
              <div class="card--footer">
                <v-icon left large :color="iconColor">mdi-dots-hexagon</v-icon>
                <span>{{ $t('categories.pm10') }}</span>
                <i class="flex-grow-1"></i>
                <span>{{ $t('values.pm10', [device.pm10]) }}</span>
              </div>
            </div>
          </v-col>

          <v-col cols="6">
            <div :class="`card  ${stateClassPm2_5}`">
              <div class="card--body">
                <span>{{ stateNamePm2_5 }}</span>
              </div>
              <div class="card--footer">
                <v-icon left large :color="iconColor">mdi-blur</v-icon>
                <span>{{ $t('categories.pm2_5') }}</span>
                <i class="flex-grow-1"></i>
                <span>{{ $t('values.pm2_5', [device.pm2_5]) }}</span>
              </div>
            </div>
          </v-col>

          <v-col cols="6">
            <div :class="`card  ${stateClassCo2}`">
              <div class="card--body">
                <span>{{ stateNameCo2 }}</span>
              </div>
              <div class="card--footer">
                <v-icon left large :color="iconColor">mdi-molecule-co2</v-icon>
                <span>{{ $t('categories.co2') }}</span>
                <i class="flex-grow-1"></i>
                <span>{{ $t('values.co2', [device.co2]) }}</span>
              </div>
            </div>
          </v-col>

          <v-col cols="6">
            <div :class="`card  ${stateClassVoc}`">
              <div class="card--body">
                <span>{{ stateNameVoc }}</span>
              </div>
              <div class="card--footer">
                <span class="text-h6 font-weight-bold text-no-wrap mr-2">VOC</span>
                <span>{{ $t('categories.voc') }}</span>
                <i class="flex-grow-1"></i>
                <span>{{ $t('values.voc', [device.voc]) }}</span>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </div>

    <!-- Add Dialog -->
    <v-dialog
      v-model="showSelectDeviceDialog"
      persistent
      no-click-animation
      :max-width="widthDialog"
      @keydown.esc.stop="onClickSelectDeviceCancel"
    >
      <v-card>
        <v-card-title class="mb-1">{{ $t('title.selectDialog') }}</v-card-title>
        <v-card-subtitle>{{ $t('subtitle.selectDialog') }}</v-card-subtitle>

        <v-divider></v-divider>

        <v-container>
          <v-select
            dense
            outlined
            :value="device"
            @input="onInputDevice"
            :rules="uidRules"
            :items="devices"
            item-text="name"
            item-value="uid"
            return-object
          >
            <template v-slot:item="{item}">
              {{ item.name }}
              <v-chip class="ml-2" x-small outlined color="primary">
                <v-icon left>mdi-identifier</v-icon>
                {{ item.uid }}
              </v-chip>
            </template>

            <template v-slot:selection="{item}">
              {{ item.name }}
              <v-chip class="ml-2" x-small outlined color="primary">
                <v-icon left>mdi-identifier</v-icon>
                {{ item.uid }}
              </v-chip>
            </template>
          </v-select>
        </v-container>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="second" class="mr-1" @click="onClickSelectDeviceCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
            :loading="submitLoading"
            color="primary"
            @click="onClickSelectDeviceOk"
          >
            {{ $t('ok') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-speed-dial
      v-model="fab"
      class="fab-layout"
      direction="top"
      transition="slide-y-reverse-transition"
    >
      <template v-slot:activator>
        <v-btn elevation="3" fab x-small icon>
          <v-icon v-if="fab">mdi-close</v-icon>
          <v-icon v-else>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>

      <v-btn fab x-small @click="onClickFullscreen">
        <v-icon v-if="fullscreenMode">mdi-fullscreen-exit</v-icon>
        <v-icon v-else>mdi-fullscreen</v-icon>
      </v-btn>
      <v-btn fab x-small @click="onClickSelectDevice">
        <v-icon>mdi-tablet</v-icon>
      </v-btn>
    </v-speed-dial>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TitleLogoSmall from '@/components/TitleLogoSmall.vue';
import {
  State,
  AirjoyDeviceA,
  getStateByPm10,
  getStateByPm2_5,
  getStateByCo2,
  getStateByVoc,
  calcHumidityText as _calcHumidityText,
  calcTemperature as _calcTemperature,
} from '@/packet/airjoy';
import requiredField from '@/rules/required';
import AxiosLib from 'axios';
import {Moment} from 'moment-timezone';
import {createMoment} from '@/chrono/date';

function createAxios() {
  return AxiosLib.create({
    baseURL: document.location.origin,
    validateStatus: (status: number): boolean => {
      return 200 === status;
    },
  });
}

function getHtmlOverflow() {
  const html = document.getElementsByTagName('html')[0];
  return html.style.overflow;
}

function setHtmlOverflow(value: string) {
  const html = document.getElementsByTagName('html')[0];
  html.style.overflow = value;
}

function hiddenHtmlOverflow() {
  setHtmlOverflow('hidden');
}

@Component({
  components: {
    TitleLogoSmall,
  },
})
export default class MainAirjoySummary extends VueBase {
  private readonly uidRules = [requiredField];

  @Prop({type: String, default: '128px'})
  readonly logoMinWidth!: string;

  @Prop({type: String, default: '68px'})
  readonly logoMinHeight!: string;

  @Prop({type: Number, default: 1000})
  readonly updateIntervalMilliseconds!: number;

  @Prop({type: Number, default: 480})
  readonly widthDialog!: number;

  @Ref('video-player')
  videoPlayer!: HTMLVideoElement;

  originalHtmlOverflow = '';
  originalBarHide = false;
  originalBarNavi = false;
  originalNaviHide = false;

  fullscreenMode = false;
  fab = false;

  playlist = [] as Array<string>;

  intervalHandle = -1;

  showSelectDeviceDialog = false;
  loadingDevices = false;
  devices = [] as Array<AirjoyDeviceA>;
  device = {} as AirjoyDeviceA;
  submitLoading = false;

  now!: Moment;
  nowDate = '';
  nowTime = '';

  private formatDate(m: Moment) {
    const momentFormat = this.$t('format.date').toString();
    return m.format(momentFormat);
  }

  private formatTime(m: Moment) {
    const momentFormat = this.$t('format.time').toString();
    return m.clone().locale('en').format(momentFormat);
  }

  get deviceName() {
    return this.device.name || this.$t('msg.selectDevice');
  }

  get iconColor() {
    if (this.$vuetify.theme.dark) {
      return 'white';
    } else {
      return 'black';
    }
  }

  getStateName(state: State) {
    switch (state) {
      case State.Good:
        return this.$t('state.good');
      case State.Normal:
        return this.$t('state.normal');
      case State.Warning:
        return this.$t('state.warning');
      case State.Danger:
        return this.$t('state.danger');
      default:
        return this.$t('state.unknown');
    }
  }

  getStateClass(state: State) {
    switch (state) {
      case State.Good:
        return 'state--good';
      case State.Normal:
        return 'state--normal';
      case State.Warning:
        return 'state--warning';
      case State.Danger:
        return 'state--danger';
      default:
        return '';
    }
  }

  get statePm10() {
    return getStateByPm10(this.device.pm10);
  }

  get statePm2_5() {
    return getStateByPm2_5(this.device.pm2_5);
  }

  get stateCo2() {
    return getStateByCo2(this.device.co2);
  }

  get stateVoc() {
    return getStateByVoc(this.device.voc);
  }

  get stateNamePm10() {
    return this.getStateName(this.statePm10);
  }

  get stateNamePm2_5() {
    return this.getStateName(this.statePm2_5);
  }

  get stateNameCo2() {
    return this.getStateName(this.stateCo2);
  }

  get stateNameVoc() {
    return this.getStateName(this.stateVoc);
  }

  get stateClassPm10() {
    return this.getStateClass(this.device.pm10);
  }

  get stateClassPm2_5() {
    return this.getStateClass(this.device.pm2_5);
  }

  get stateClassCo2() {
    return this.getStateClass(this.device.co2);
  }

  get stateClassVoc() {
    return this.getStateClass(this.device.voc);
  }

  calcHumidityText(value: number) {
    return _calcHumidityText(value);
  }

  calcTemperature(value: number) {
    return _calcTemperature(value);
  }

  created() {
    this.now = createMoment();
    this.nowDate = this.formatDate(this.now);
    this.nowTime = this.formatTime(this.now);

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loadingDevices = true;
    this.$api2
      .getAirjoyDevices(group, project)
      .then(items => {
        this.loadingDevices = false;
        this.devices = items;
      })
      .catch(error => {
        this.loadingDevices = false;
        this.toastRequestFailure(error);
      });

    const mediaPrefix = `/app/media/airjoy/${group}/${project}`;
    const defaultMedia = `/app/media/airjoy/default.mp4`;
    createAxios()
      .get<string>(`${mediaPrefix}/playlist`)
      .then(text => {
        this.playlist = text.data.split('\n').map(x => mediaPrefix + '/' + x.trim());
        this.playVideo();
      })
      .catch(error => {
        this.playlist = [defaultMedia];
        this.playVideo();
      });
  }

  mounted() {
    this.videoPlayer.addEventListener('ended', this.onVideoEnded);
    this.intervalHandle = window.setInterval(() => {
      this.updateDevice();
    }, this.updateIntervalMilliseconds);

    this.originalHtmlOverflow = getHtmlOverflow();
    this.originalBarHide = this.$localStore.barHide;
    this.originalBarNavi = this.$localStore.barNavi;
    this.originalNaviHide = this.$localStore.naviHide;
  }

  beforeDestroy() {
    this.videoPlayer.removeEventListener('ended', this.onVideoEnded);
    window.clearInterval(this.intervalHandle);

    setHtmlOverflow(this.originalHtmlOverflow);
    this.$localStore.barHide = this.originalBarHide;
    this.$localStore.barNavi = this.originalBarNavi;
    this.$localStore.naviHide = this.originalNaviHide;
  }

  updateDevice() {
    this.now = createMoment();
    this.nowDate = this.formatDate(this.now);
    this.nowTime = this.formatTime(this.now);

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2
      .getAirjoyLive(group, project)
      .then(items => {
        this.toastRequestSuccess();
      })
      .catch(error => {
        // this.toastRequestFailure(error);
      });
  }

  playVideo(index = 0) {
    this.videoPlayer.src = this.playlist[index];
    this.videoPlayer.load();
    this.videoPlayer.play();
  }

  onVideoEnded() {
    const currentIndex = this.playlist.indexOf(this.videoPlayer.src);

    let nextIndex: number;
    if (currentIndex + 1 >= this.playlist.length) {
      nextIndex = 0;
    } else {
      nextIndex = currentIndex + 1;
    }

    this.playVideo(nextIndex);
  }

  enterFullscreen() {
    this.fullscreenMode = true;
    this.$localStore.barHide = true;
    this.$localStore.barNavi = true;
    this.$localStore.naviHide = true;
    hiddenHtmlOverflow();
  }

  exitFullscreen() {
    this.fullscreenMode = false;
    this.$localStore.barHide = false;
    this.$localStore.barNavi = false;
    this.$localStore.naviHide = false;
    setHtmlOverflow(this.originalHtmlOverflow);
  }

  onClickFullscreen() {
    if (this.fullscreenMode) {
      this.exitFullscreen();
    } else {
      this.enterFullscreen();
    }
  }

  onClickSelectDevice() {
    this.showSelectDeviceDialog = true;
  }

  onClickSelectDeviceCancel() {
    this.showSelectDeviceDialog = false;
  }

  onClickSelectDeviceOk() {}

  onInputDevice(value) {
    this.device = value;
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

.video-player {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.date-text {
  font-family: $body-font-family;
  font-size: 2.2rem;
  font-weight: 300;
  line-height: 4rem;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.time-text {
  font-family: $body-font-family;
  font-size: 5rem;
  font-weight: 300;
  line-height: 4rem;
  letter-spacing: -0.015625em;
  white-space: nowrap;
}

.fab-layout {
  position: fixed;
  right: 16px;
  bottom: 16px;
}

@mixin headings-nowrap($var) {
  font-family: map-deep-get($headings, $var, 'font-family');
  font-size: map-deep-get($headings, $var, 'size');
  font-weight: map-deep-get($headings, $var, 'weight');
  line-height: map-deep-get($headings, $var, 'line-height');
  letter-spacing: map-deep-get($headings, $var, 'letter-spacing');
  white-space: nowrap;
}

.card {
  display: flex;
  flex-direction: column;

  background-color: #f2f2f0;

  border-radius: 24px;
  border-style: solid;
  border-width: 8px;

  cursor: pointer;

  .card--body {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    min-height: 320px;

    @include headings-nowrap('h1');
  }

  .card--footer {
    display: flex;
    flex-direction: row;
    align-items: center;

    padding: 0 24px;
    min-height: 48px;

    @include headings-nowrap('h6');
  }
}

.state--good {
  border-color: #1285c8;
}
.state--normal {
  border-color: #6fb747;
}
.state--warning {
  border-color: #f9e04b;
}
.state--danger {
  border-color: #e9434c;
}

.theme--light.v-application {
  .video-player {
    background-color: map-get($grey, 'base');
  }
}

.theme--dark.v-application {
  .video-player {
    background-color: map-get($grey, 'darken-2');
  }
}
</style>
