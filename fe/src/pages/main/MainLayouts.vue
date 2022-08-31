<i18n lang="yaml">
en:
  menus:
    widgets: 'Widgets'
  tools:
    layouts: 'Layouts'
    new_layouts: 'New Layout'
    widgets: 'Widgets'
    fullscreen: 'Fullscreen'
  widgets:
    jupyter: 'Jupyter'
    movie: 'Movie'
    music: 'Music'
    button: 'Button'
    switch: 'Switch'
    web: 'Web'
    table: 'Table'
    webcam: 'Webcam'
  msg:
    unselected: 'Unselected layout.'
    empty: 'Empty Layouts.'

ko:
  menus:
    widgets: '위젯'
  tools:
    layouts: '레이아웃'
    new_layouts: '새로운 레이아웃'
    widgets: '위젯'
    fullscreen: '전체화면'
  widgets:
    jupyter: '주피터'
    movie: '비디오 재생'
    music: '음악 재생'
    button: '버튼 이벤트'
    switch: '스위치'
    web: '외부 사이트'
    table: '라이브 테이블'
    webcam: '웹캠 녹화'
  msg:
    unselected: '선택된 레이아웃이 없습니다.'
    empty: '레이아웃이 존재하지 않습니다.'
</i18n>

<template>
  <div>
    <v-navigation-drawer
      right
      app
      clipped
      permanent
      stateless
      touchless
      :mini-variant.sync="miniWidgets"
    >
      <v-list nav dense>
        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>mdi-widgets</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('menus.widgets') }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>

        <v-list-item link @click.stop="onClickJupyter">
          <v-list-item-icon>
            <v-icon>mdi-language-python</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.jupyter') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickMovie">
          <v-list-item-icon>
            <v-icon>mdi-movie-open-play</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.movie') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickMusic">
          <v-list-item-icon>
            <v-icon>mdi-music</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.music') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickButton">
          <v-list-item-icon>
            <v-icon>mdi-cursor-default-click</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.button') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickSwitch">
          <v-list-item-icon>
            <v-icon>mdi-electric-switch</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.switch') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickWeb">
          <v-list-item-icon>
            <v-icon>mdi-web</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.web') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickWebcam">
          <v-list-item-icon>
            <v-icon>mdi-webcam</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.webcam') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="onClickTable">
          <v-list-item-icon>
            <v-icon>mdi-table</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('widgets.table') }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar dense flat>
      <v-btn plain small @click="onClickLayouts">
        <v-icon left>mdi-view-dashboard</v-icon>
        {{ $t('tools.layouts') }}
      </v-btn>

      <v-btn plain small @click="onClickLayouts">
        <v-icon left>mdi-widgets</v-icon>
        {{ $t('tools.widgets') }}
      </v-btn>

      <v-btn plain small @click="onClickLayouts">
        <v-icon left>mdi-fullscreen</v-icon>
        {{ $t('tools.fullscreen') }}
      </v-btn>

      <v-btn icon plain small @click="onClickMore">
        <v-icon>mdi-dots-horizontal</v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>

    <view-port class="d-flex flex-row align-center justify-center">
      <div class="d-flex flex-column align-center justify-center">
        <v-icon x-large>mdi-view-dashboard</v-icon>
        <span class="text--secondary text-subtitle-2">
          {{ $t('msg.empty') }}
        </span>
      </div>
    </view-port>
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    BreadcrumbMain,
    ViewPort,
  },
})
export default class MainLayouts extends VueBase {
  @Ref()
  readonly root!: HTMLDivElement;

  miniWidgets = false;

  mounted() {
    // this.window0 = new WinBox('Demo Window', {root: this.root});
  }

  onClickFoldNavigation() {
    this.miniWidgets = !this.miniWidgets;
  }

  onClickLayouts() {}

  onClickMore() {}

  onClickJupyter() {
    // this.window1 = new WinBox('Jupyter', {root: this.root});
  }

  onClickMovie() {}

  onClickMusic() {}

  onClickButton() {}

  onClickSwitch() {}

  onClickWeb() {}

  onClickWebcam() {}

  onClickTable() {}
}
</script>
