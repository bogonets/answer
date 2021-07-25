<i18n lang="yaml">
en:
  title: "Admin Preference"
  overview: "Overview"

ko:
  title: "관리자 설정"
  overview: "개요"
</i18n>

<template>
  <v-container>

    <v-navigation-drawer
        app
        clipped
        permanent
        stateless
        touchless
        :mini-variant.sync="miniNavigation"
    >
      <v-list nav dense>

        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>{{ icons.cogOutline }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('title') }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>{{ icons.chevronLeft }}</v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item-group
            mandatory
            color="primary"
            :value="currentSubpageIndex"
        >

          <v-list-item link @click.stop="onClickOverview">
            <v-list-item-icon>
              <v-icon>{{ icons.viewList }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('overview') }}
            </v-list-item-title>
          </v-list-item>

        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <router-view>
    </router-view>

  </v-container>
</template>

<script lang="ts">
import VueI18n from '@/translations/VueI18n';
import { Component } from 'vue-property-decorator';
import { mdiCogOutline, mdiChevronLeft, mdiViewList } from '@mdi/js';

@Component
export default class ConfigAdminPage extends VueI18n {

  readonly icons = {
    cogOutline: mdiCogOutline,
    chevronLeft: mdiChevronLeft,
    viewList: mdiViewList,
  };

  currentSubpageIndex = 0;
  miniNavigation = false;

  mounted() {
    this.moveOverview();
  }

  moveOverview() {
    const movePath = '/main/config/admin/overview';
    if (this.$router.currentRoute.path !== movePath) {
      this.$router.push(movePath);
    }
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickOverview() {
    this.moveOverview();
  }
}
</script>
