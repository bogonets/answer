<i18n lang="yaml">
en:
  menu:
    setting: "Setting"

ko:
  menu:
    setting: "설정"
</i18n>

<template>
  <div class="d-flex flex-column fill-height">
    <div class="d-flex flex-wrap main">
      <media-player
          v-for="i in maxCards"
          :key="`${i}-${loading}`"
          :style="cardStyle(i)"
          :group="$route.params.group"
          :project="$route.params.project"
          :device="getDeviceUid(i)"
          :loading="loading"
          @contextmenu="onShowContextMenu(i, $event)"
      ></media-player>
    </div>

    <v-footer>
      <v-system-bar absolute>
        <v-icon>mdi-application</v-icon>
        <v-spacer></v-spacer>
        <v-btn icon small max-width="22px" max-height="22px" @click="onClickCloseFooter">
          <v-icon small class="ma-0">mdi-close</v-icon>
        </v-btn>
      </v-system-bar>
      <v-sheet :height="footerHeight">

      </v-sheet>
    </v-footer>

    <v-menu
        v-model="showContextMenu"
        :position-x="contextMenuPositionX"
        :position-y="contextMenuPositionY"
        absolute
        offset-y
        z-index="100"
    >
      <v-list dense>
        <v-list-item @click="onClickEdit">
          <v-list-item-title>{{ $t('menu.setting') }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import type {VmsDeviceA, VmsLayoutA} from '@/packet/vms';

@Component({
  components: {
    MediaPlayer,
  }
})
export default class MainVmsLive extends VueBase {
  readonly footerHeight = 200;

  maxCards = 4;
  showFooter = true;

  showContextMenu = false;
  contextMenuIndex = 0;
  contextMenuPositionX = 0;
  contextMenuPositionY = 0;

  loading = false;

  layouts = [] as Array<VmsLayoutA>;
  devices = [] as Array<VmsDeviceA>;

  layoutToDevice = {};

  created() {
    this.requestSetup();
  }

  requestSetup() {
    this.loading = true;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      this.layouts = await this.$api2.getVmsLayouts(group, project);
      this.devices = await this.$api2.getVmsDevices(group, project);

      const layoutToDevice = {};
      for (let i = 0; i < this.maxCards; ++i) {
        const layout = this.layouts.find(l => l.index == i);
        if (typeof layout === 'undefined') {
          continue;
        }
        const device = this.devices.find(d => d.device_uid === layout.device_uid);
        if (typeof device === 'undefined') {
          continue;
        }

        layoutToDevice[i] = device;
      }
      this.layoutToDevice = layoutToDevice;
      console.dir(this.layoutToDevice);

    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  cardStyle(index: number) {
    // return {
    //   width: '33.333%',
    //   height: '33.333%',
    // };
    return {
      width: '50%',
      height: '50%',
    };
  }

  getDeviceUid(index: number) {
    const layoutIndex = index - 1;
    const device = this.layoutToDevice[layoutIndex] as VmsDeviceA;
    if (typeof device === 'undefined') {
      return undefined;
    }
    return device.device_uid;
  }

  onShowContextMenu(index: number, event) {
    event.preventDefault();
    this.showContextMenu = false;
    this.contextMenuIndex = index;
    this.contextMenuPositionX = event.clientX;
    this.contextMenuPositionY = event.clientY;
    this.$nextTick(() => {
      this.showContextMenu = true;
    })
  }

  onClickEdit() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const index = this.contextMenuIndex;
    // this.moveToMainVmsDevicesEdit(group, project, media);
  }

  onClickCloseFooter() {
    this.showFooter = false;
  }
}
</script>

<style lang="scss" scoped>
.fill-height {
  height: 100%;
}

.main {
  flex: auto;
}
</style>
