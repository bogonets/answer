<i18n lang="yaml">
en:
  title: "Video management system"
  subtitle: "Browse the files in the project workspace."

ko:
  title: "지능형 영상 분석 시스템"
  subtitle: "프로젝트 작업공간의 파일을 탐색합니다."
</i18n>

<template>
  <v-container class="pa-0 fill-width">
    <v-system-bar></v-system-bar>

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
          <v-list-item-title>
            {{ project }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>
      </v-list>
    </v-navigation-drawer>

    <v-container class="pa-0 fill-width d-flex flex-wrap" :style="contentStyle">
      <v-card v-for="n in 4" :key="n" outlined tile width="200" height="200">
        {{ `Column-${n}` }}
      </v-card>
    </v-container>

  </v-container>
</template>

<script lang="ts">
import {Component, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

const TOOLBAR_HEIGHT = 48;
const SYSTEM_BAR_HEIGHT = 24;

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class VmsPage extends VueBase {

  windowWidth = window.innerWidth;
  windowHeight = window.innerHeight;

  navigationItems: object = [];
  miniNavigation = false;

  @Watch('windowWidth')
  updateWindowWidth(newVal: string, oldVal: string) {
    console.debug(`Update width: ${oldVal} -> ${newVal}`);
  }

  @Watch('windowHeight')
  updateWindowHeight(newVal: string, oldVal: string) {
    console.debug(`Update height: ${oldVal} -> ${newVal}`);
  }

  get group(): string {
    return this.$route.params.group;
  }

  get project(): string {
    return this.$route.params.project;
  }

  get contentStyle() {
    const height = this.windowHeight - TOOLBAR_HEIGHT - SYSTEM_BAR_HEIGHT;
    return {height: `${height}px`};
  }

  created() {
    this.navigationItems = [
      {
        text: 'Projects',
        disabled: false,
        href: this.paths.mainProjects,
      },
      {
        text: this.project,
        disabled: false,
        href: this.paths.mainProjects,
      },
      {
        text: 'VMS',
        disabled: true,
      },
    ];
  }

  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
    })
  }

  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  }

  onResize() {
    this.windowWidth = window.innerWidth;
    this.windowHeight = window.innerHeight;
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }
}
</script>

<style lang="scss" scoped>
.fill-width {
  max-width: 100%;
}
</style>
