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
  <v-container class="pa-0 fill-width">
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

    <v-container class="pa-0 fill-width d-flex flex-wrap" :style="contentStyle">
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
    </v-container>

    <v-footer absolute padless height="200px">
      <v-system-bar absolute>
        <v-icon>mdi-application</v-icon>
        <v-spacer></v-spacer>
        <v-btn icon small max-width="22px" max-height="22px">
          <v-icon small class="ma-0">mdi-close</v-icon>
        </v-btn>
      </v-system-bar>
      <v-col class="text-center" cols="12">Control Panel</v-col>
    </v-footer>

  </v-container>
</template>

<script lang="ts">
import {Component, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

const TOOLBAR_HEIGHT = 48;
const FOOTER_HEIGHT = 200;

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class MainVms extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: 'VMS',
      disabled: true,
    },
  ];

  contentWidth = window.innerWidth;
  contentHeight = window.innerHeight;

  maxCards = 4;
  miniNavigation = false;

  @Watch('contentWidth')
  updateContentWidth(newVal: string, oldVal: string) {
    console.debug(`Update content-width: ${oldVal} -> ${newVal}`);
  }

  @Watch('contentHeight')
  updateContentHeight(newVal: string, oldVal: string) {
    console.debug(`Update content-height: ${oldVal} -> ${newVal}`);
  }

  get contentStyle() {
    return {height: `${this.contentHeight}px`};
  }

  cardStyle(index: number) {
    const halfHeight = this.contentHeight * 0.5;
    return {
      width: '50%',
      height: '50%',
    };
  }

  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
      this.onResize();
    })
  }

  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  }

  onResize() {
    this.contentWidth = window.innerWidth;
    this.contentHeight = window.innerHeight - TOOLBAR_HEIGHT - FOOTER_HEIGHT;
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

.absolute-position {
  position: absolute;
  //position: fixed;
  //transform: translateX(0%);
}

.disconnected-background {
  background: gray;
}
</style>
