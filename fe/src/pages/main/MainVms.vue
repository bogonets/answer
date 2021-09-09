<i18n lang="yaml">
en:
  title: "Video management system"
  subtitle: "Browse the files in the project workspace."
  menu: "VMS Menu"
  cameras: "Cameras"

ko:
  title: "지능형 영상 분석 시스템"
  subtitle: "프로젝트 작업공간의 파일을 탐색합니다."
  menu: "VMS 메뉴"
  cameras: "카메라"
</i18n>

<template>
  <div>
    <v-navigation-drawer
        app
        right
        clipped
        permanent
        stateless
        touchless
        :mini-variant.sync="miniNavigation"
    >
      <v-list nav dense>

        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>mdi-menu</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('menu') }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item link @click.stop="onClickCameras">
          <v-list-item-icon>
            <v-icon>mdi-webcam</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('cameras') }}
          </v-list-item-title>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>

    <view-port
        class="d-flex flex-wrap"
        :margin-bottom="footerHeight"
    >
      <v-card
          v-for="i in maxCards"
          :key="i"
          outlined
          tile
          class="disconnected-background"
          :style="cardStyle(i)"
      >
        <div class="pa-0 fill-height d-flex align-center justify-center">
          <v-system-bar absolute lights-out>
            <v-icon small color="red">mdi-record</v-icon>
            {{ `CCTV ${i}` }}
            <v-spacer></v-spacer>
            <v-icon>mdi-video-4k-box</v-icon>
            <v-icon>mdi-video-off</v-icon>
            <v-icon>mdi-volume-off</v-icon>
            <v-icon>mdi-signal-cellular-outline</v-icon>
          </v-system-bar>
          <v-img src="@/assets/logo/answer-logo-notext.svg" max-width="200px" max-height="200px" contain></v-img>
        </div>
      </v-card>
    </view-port>

    <v-footer :height="footerHeight">
      <v-system-bar absolute>
        <v-icon>mdi-application</v-icon>
        <v-spacer></v-spacer>
        <v-btn icon small max-width="22px" max-height="22px">
          <v-icon small class="ma-0">mdi-close</v-icon>
        </v-btn>
      </v-system-bar>
      <v-col class="text-center" cols="12">Control Panel</v-col>
    </v-footer>

  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    ViewPort,
  }
})
export default class MainVms extends VueBase {
  readonly footerHeight = 200;

  maxCards = 4;
  miniNavigation = false;

  cardStyle(index: number) {
    return {
      width: '50%',
      height: '50%',
    };
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickCameras() {
  }
}
</script>

<style lang="scss" scoped>
.fill-width {
  max-width: 100%;
}

.disconnected-background {
  background: gray;
}
</style>
