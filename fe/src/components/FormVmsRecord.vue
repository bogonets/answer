<i18n lang="yaml">
en:
  labels:
    toady: "Today"

ko:
  labels:
    toady: "오늘"
</i18n>

<template>
  <div class="d-flex flex-column">
    <hls-player
        ref="hls-player"
        :src="hlsUrl"
        :options="hlsOptions"
        :group="$route.params.group"
        :project="$route.params.project"
        :device="$route.params.device"
        :online="!disabled"
    ></hls-player>

    <div class="controllers">
      <div class="left-controller">
        <v-menu
            offset-y
            transition="scale-transition"
            min-width="auto"
            v-model="showDateMenu"
            :nudge-right="datePickerSize"
            :close-on-content-click="false"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                icon
                v-bind="attrs"
                v-on="on"
            >
              <v-icon>mdi-calendar</v-icon>
            </v-btn>
          </template>
          <v-date-picker
              no-title
              scrollable
              v-model="date"
              :min="begin"
              :max="end"
              :allowed-dates="allowedDates"
              @input="onInputDate"
          ></v-date-picker>
        </v-menu>
        <span class="mr-2 text--secondary text-caption">{{ date }}</span>
        <v-btn color="secondary" outlined rounded x-small @click="onClickToday">
          {{ $t('labels.toady') }}
        </v-btn>
      </div>

      <div class="center-controller">
        <v-btn
            class="mr-2"
            icon
            outlined
            small
            :disabled="disabled"
            @click="onClickFirst"
        >
          <v-icon small>mdi-skip-backward</v-icon>
        </v-btn>
        <v-btn
            class="mr-2"
            icon
            outlined
            :disabled="disabled"
            @click="onClickPrevious"
        >
         <v-icon>mdi-skip-previous</v-icon>
        </v-btn>
        <v-btn
            class="mr-2"
            icon
            large
            outlined
            :disabled="disabled"
            @click="onClickPlay"
        >
          <v-icon large>{{ playIcon }}</v-icon>
        </v-btn>
        <v-btn
            class="mr-2"
            icon
            outlined
            :disabled="disabled"
            @click="onClickNext"
        >
          <v-icon>mdi-skip-next</v-icon>
        </v-btn>
        <v-btn
            icon
            outlined
            small
            :disabled="disabled"
            @click="onClickLast"
        >
          <v-icon small>mdi-skip-forward</v-icon>
        </v-btn>
      </div>

      <div class="right-controller">
      </div>
    </div>

    <record-controller
        class="mt-2"
        :disabled="disabled"
        @click="onClickRecordController"
    >
    </record-controller>

    <div class="d-flex flex-row">
      <span class="text--secondary text-overline">00:00:00</span>
      <v-spacer></v-spacer>
      <span class="text--secondary text-overline">23:59:59</span>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Watch, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import HlsPlayer from '@/media/HlsPlayer.vue';
import RecordController from '@/media/RecordController.vue';
import {todayString} from '@/chrono/date';

@Component({
  components: {
    HlsPlayer,
    RecordController,
  }
})
export default class FormVmsRecord extends VueBase {
  @Prop({type: String, default: ''})
  readonly group!: string;

  @Prop({type: String, default: ''})
  readonly project!: string;

  @Prop({type: [String, Number]})
  readonly device?: string | number;

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  @Ref('hls-player')
  readonly hlsPlayer!: HlsPlayer;

  hlsUrl = '';
  hlsOptions = {};

  play = false;
  recordDates = [] as Array<string>;

  showDateMenu = false;
  begin = '';
  end = '';
  date = '';

  disabled = true;

  mounted() {
    if (typeof this.$route.params.date !== 'undefined') {
      this.date = this.$route.params.date;
    } else {
      this.date = todayString();
    }

    this.hlsOptions = {
      xhrSetup: this._xhrSetup,
      licenseXhrSetup: this._licenseXhrSetup,
    };

    this.$api2.getVmsRecordsPdeviceDates(this.group, this.project, this.deviceText)
        .then(items => {
          this.recordDates = items;
          console.debug('record dates:', this.recordDates)
          if (items) {
            this.begin = items[0];
            this.end = items[items.length - 1];

            this.updateDate(this.date);
          } else {
            this.begin = '';
            this.end = '';
          }
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  _xhrSetup(xhr: XMLHttpRequest, url: string) {
    const bearerToken = `Bearer ${this.$localStore.access}`;
    xhr.setRequestHeader('Authorization', bearerToken);
  }

  _licenseXhrSetup(xhr: XMLHttpRequest, url: string) {
    const bearerToken = `Bearer ${this.$localStore.access}`;
    xhr.setRequestHeader('Authorization', bearerToken);
  }

  get deviceNumber() {
    if (typeof this.device === 'undefined') {
      return 0;
    } else if (typeof this.device === 'string') {
      return Number.parseInt(this.device);
    } else {
      return this.device;
    }
  }

  get deviceText() {
    if (typeof this.device === 'undefined') {
      return '';
    } else if (typeof this.device === 'string') {
      return this.device;
    } else {
      return this.device.toString();
    }
  }

  get playIcon() {
    if (this.play) {
      return 'mdi-pause';
    } else {
      return 'mdi-play';
    }
  }

  get dateStart() {
    return `${this.date}T00:00:00.000`;
  }

  get dateLast() {
    return `${this.date}T23:59:59.999`;
  }

  @Watch('date')
  watchDate(newVal: string) {
    this.updateDate(newVal);
  }

  updateDate(date: string) {
    this.disabled = !this.recordDates.includes(date);
    if (!this.disabled) {
      this.hlsUrl = this.$api2.urlVmsRecordsPdevicePlaylistMaster(
          this.group,
          this.project,
          this.deviceText,
          this.dateStart,
          this.dateLast,
      );
    }
    console.debug(`updateDate('${date}') -> ${this.disabled ? "disabled" : "exists!"}`);
    console.debug('HLS URL: ', this.hlsUrl);
  }

  allowedDates(value: string) {
    return this.recordDates.includes(value);
  }

  onInputDate() {
    this.showDateMenu = true;
  }

  onClickToday() {
    this.date = todayString();
  }

  onClickFirst() {
  }

  onClickPrevious() {
  }

  onClickPlay() {
    this.hlsPlayer.play();
  }

  onClickNext() {
  }

  onClickLast() {
  }

  onClickRecordController(pos: number) {
    console.assert(0 <= pos && pos <= 1);
    console.debug(`onClickRecordController(pos=${pos})`)
  }
}
</script>

<style lang="scss" scoped>
.controllers {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  padding: 4px;
  margin: 8px 0 0 0;

  width: 100%;

  .left-controller {
    position: absolute;
    left: 0;
  }

  .center-controller {
  }

  .right-controller {
    position: absolute;
    right: 0;
  }
}
</style>
