<i18n lang="yaml">
en:
  configs: "Configs"

ko:
  configs: "구성"
</i18n>

<template>
  <v-container>

    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-list flat subheader three-line>
      <v-subheader>{{ $t('theme.header') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('theme.dark.title') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('theme.dark.subtitle') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-switch inset></v-switch>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>{{ $t('i18n.header') }}</v-subheader>

<!--      <v-list-item>-->
<!--        <v-list-item-content>-->
<!--          <v-list-item-title>{{ $t('i18n.lang.title') }}</v-list-item-title>-->
<!--          <v-list-item-subtitle>{{ $t('i18n.lang.subtitle') }}</v-list-item-subtitle>-->
<!--        </v-list-item-content>-->

<!--        <v-menu transition="slide-y-transition" :offset-y="true">-->
<!--          <template v-slot:activator="{ on, attrs }">-->
<!--            <v-btn v-bind="attrs" v-on="on">-->
<!--              {{ currentLangName }}-->
<!--              <v-icon right role="img" aria-hidden="false">-->
<!--                mdi-chevron-down-->
<!--              </v-icon>-->
<!--            </v-btn>-->
<!--          </template>-->
<!--          <list-languages-->
<!--              :init-lang="extra.lang"-->
<!--              @change-lang="changeLang"-->
<!--          ></list-languages>-->
<!--        </v-menu>-->
<!--      </v-list-item>-->

    </v-list>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';

@Component({
  components: {
    ToolbarBreadcrumbs
  }
})
export default class AdminConfigs extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Configs',
      disabled: true,
    },
  ];
}
</script>
