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
          color="grey"
          outlined
          tile
          :style="cardStyle(i)"
      >
        <media-player></media-player>
      </v-card>
    </view-port>

    <v-footer :height="footerHeight">
      <v-system-bar absolute>
        <v-icon>mdi-application</v-icon>
        <v-spacer></v-spacer>
        <v-btn icon small max-width="22px" max-height="22px" @click="onClickCloseFooter">
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
import MediaPlayer from '@/media/MediaPlayer.vue';

@Component({
  components: {
    ViewPort,
    MediaPlayer,
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

  onClickCloseFooter() {
  }
}
</script>

<style lang="scss" scoped>
.fill-width {
  max-width: 100%;
}
</style>
