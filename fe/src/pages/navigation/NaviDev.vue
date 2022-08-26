<i18n lang="yaml">
en:
  title: 'DevTools'
  overview: 'Overview'
  infos: 'Preferences'
  plugins: 'Plugins'
  configs: 'Configs'

ko:
  title: '개발 도구'
  overview: '개요'
  infos: '기본 설정'
  plugins: '플러그인'
  configs: '구성'
</i18n>

<template>
  <v-navigation-drawer
    app
    clipped
    permanent
    stateless
    touchless
    :mini-variant.sync="mini"
  >
    <v-list nav dense>
      <v-list-item link @click.stop="onClickFoldNavigation">
        <v-list-item-icon>
          <v-icon>mdi-dev-to</v-icon>
        </v-list-item-icon>
        <v-list-item-title>
          {{ $t('title') }}
        </v-list-item-title>
        <v-btn icon @click.stop="onClickFoldNavigation">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </v-list-item>

      <v-divider></v-divider>

      <v-list-item-group mandatory color="primary" :value="index" @change="input">
        <v-list-item link @click.stop="overview">
          <v-list-item-icon>
            <v-icon>mdi-developer-board</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('overview') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="infos">
          <v-list-item-icon>
            <v-icon>mdi-cogs</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('infos') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="plugins">
          <v-list-item-icon>
            <v-icon>mdi-toy-brick</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('plugins') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="configs">
          <v-list-item-icon>
            <v-icon>mdi-format-list-checks</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('configs') }}
          </v-list-item-title>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import {Component, Prop, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import devNames from '@/router/names/dev';

@Component
export default class NaviDev extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  mini = false;
  index = 0;

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Watch('$route')
  onChangeRoute() {
    const name = this.$route.name;
    if (name === devNames.devOverview) {
      this.index = 0;
    } else if (name === devNames.devInfos) {
      this.index = 1;
    } else if (name === devNames.devPlugins) {
      this.index = 2;
    } else if (name === devNames.devConfigs) {
      this.index = 3;
    } else {
      this.index = -1;
    }
  }

  @Emit()
  input(index: number) {
    this.index = index;
    return index;
  }

  @Emit('click:overview')
  overview() {
    if (!this.noDefault) {
      this.moveToDev();
    }
  }

  @Emit('click:infos')
  infos() {
    if (!this.noDefault) {
      this.moveToDevInfos();
    }
  }

  @Emit('click:plugins')
  plugins() {
    if (!this.noDefault) {
      this.moveToDevPlugins();
    }
  }

  @Emit('click:configs')
  configs() {
    if (!this.noDefault) {
      this.moveToDevConfigs();
    }
  }
}
</script>
