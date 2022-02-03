<i18n lang="yaml">
en:
  submit: "Submit"

ko:
  submit: "제출"
</i18n>

<template>
  <div class="d-flex flex-column">
    <hls-player
        :src="hlsUrl"
        :options="hlsOptions"
        :group="$route.params.group"
        :project="$route.params.project"
        :device="$route.params.device"
    ></hls-player>

<!--    ma-2 d-flex flex-row justify-center align-center">-->
    <div class="controllers">
      <div class="left-controller">
        <v-btn class="mr-2" icon>
          <v-icon>mdi-calendar</v-icon>
        </v-btn>
        <span class="text--secondary text-caption">{{ now }}</span>
      </div>

      <div class="center-controller">
        <v-btn class="mr-2" icon outlined small>
          <v-icon small>mdi-skip-backward</v-icon>
        </v-btn>
        <v-btn class="mr-2" icon outlined>
          <v-icon>mdi-skip-previous</v-icon>
        </v-btn>
        <v-btn class="mr-2" icon large outlined>
          <v-icon large>{{ playIcon }}</v-icon>
        </v-btn>
        <v-btn class="mr-2" icon outlined>
          <v-icon>mdi-skip-next</v-icon>
        </v-btn>
        <v-btn icon outlined small>
          <v-icon small>mdi-skip-forward</v-icon>
        </v-btn>
      </div>

      <div class="right-controller">
      </div>
    </div>

    <record-controller class="mt-1">
    </record-controller>

    <div class="d-flex flex-row">
      <span class="text--secondary text-overline">BEGIN</span>
      <v-spacer></v-spacer>
      <span class="text--secondary text-overline">END</span>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import HlsPlayer from '@/media/HlsPlayer.vue';
import RecordController from '@/media/RecordController.vue';

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

  hlsUrl = '';
  hlsOptions = {};

  play = false;
  recordDates = [] as Array<string>;

  now = '2022-01-03';

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

  xhrSetup(xhr: XMLHttpRequest, url: string) {
    const bearerToken = `Bearer ${this.$localStore.access}`;
    xhr.setRequestHeader('Authorization', bearerToken);
  }

  licenseXhrSetup(xhr: XMLHttpRequest, url: string) {
    const bearerToken = `Bearer ${this.$localStore.access}`;
    xhr.setRequestHeader('Authorization', bearerToken);
  }

  mounted() {
    // this.hlsUrl = this.$api2.urlVmsRecords(this.group, this.project, this.deviceText);
    this.hlsOptions = {
      xhrSetup: this.xhrSetup,
      licenseXhrSetup: this.licenseXhrSetup,
    };

    this.$api2.getVmsRecordsPdeviceDates(this.group, this.project, this.deviceText)
        .then(items => {
          this.recordDates = items;
          console.dir(this.recordDates);
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
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
  margin: 0;

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
