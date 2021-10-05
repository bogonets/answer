<i18n lang="yaml">
en:
  title: "DevTools"
  overview: "Overview"
  envs: "Environment"
  infos: "Preferences"
  plugins: "Plugins"
  configs: "Configs"

ko:
  title: "개발 도구"
  overview: "개요"
  envs: "환경 변수"
  infos: "기본 설정"
  plugins: "플러그인"
  configs: "구성"
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

      <v-list-item-group
          mandatory
          color="primary"
          :value="value"
          @change="input"
      >

        <v-list-item link @click.stop="overview">
          <v-list-item-icon>
            <v-icon>mdi-developer-board</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('overview') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="envs">
          <v-list-item-icon>
            <v-icon>mdi-variable</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('envs') }}
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
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class NaviDev extends VueBase {

  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  @Prop({type: Number, default: 0})
  readonly value!: number;

  mini = false;

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Emit()
  input(index: number) {
    return index;
  }

  @Emit('click:overview')
  overview() {
    if (!this.noDefault) {
      this.moveToDev();
    }
  }

  @Emit('click:envs')
  envs() {
    if (!this.noDefault) {
      this.moveToDevEnvs();
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
