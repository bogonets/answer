<i18n lang="yaml">
en:
  tools:
    layouts: 'Layouts'
    new_layouts: 'New Layout'
    widgets: 'Widgets'
  msg:
    unselected: 'Unselected layout.'
    empty: 'Empty Layouts.'

ko:
  tools:
    layouts: '레이아웃'
    new_layouts: '새로운 레이아웃'
    widgets: '위젯'
  msg:
    unselected: '선택된 레이아웃이 없습니다.'
    empty: '레이아웃이 존재하지 않습니다.'
</i18n>

<template>
  <div>
    <v-toolbar dense flat>
      <v-btn plain small @click="onClickLayouts">
        <v-icon left>mdi-view-dashboard</v-icon>
        {{ $t('tools.layouts') }}
      </v-btn>

      <v-btn plain small @click="onClickLayouts">
        <v-icon left>mdi-widgets</v-icon>
        {{ $t('tools.widgets') }}
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
import {Component} from 'vue-property-decorator';
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
  miniNavigation = false;

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickLayouts() {}

  onClickMore() {}
}
</script>
