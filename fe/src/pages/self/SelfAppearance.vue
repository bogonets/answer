<i18n lang="yaml">
en:
  lang: "English"
  title: "Appearance"
  subtitle: "Customize the look and feel of your Answer."
  theme:
    header: "Theme"
    dark:
      title: "Dark Mode"
      subtitle: "Apply a theme that displays white text on a dark screen."
  i18n:
    header: "Internationalization"
    lang:
      title: "Language"
      subtitle: "It will be translated into your preferred language."

ko:
  lang: "한글"
  title: "외관 설정"
  subtitle: "Answer의 모양과 느낌을 설정할 수 있습니다."
  theme:
    header: "테마"
    dark:
      title: "어두운 화면"
      subtitle: "어두운 화면에 흰 글자를 나타내는 테마를 적용합니다."
  i18n:
    header: "국제화"
    lang:
      title: "언어"
      subtitle: "원하는 언어로 번역됩니다."
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

        <v-switch
            inset
            v-model="extra.dark"
            @change="changeDark"
        ></v-switch>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>{{ $t('i18n.header') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('i18n.lang.title') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('i18n.lang.subtitle') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-menu transition="slide-y-transition" :offset-y="true">
          <template v-slot:activator="{ on, attrs }">
            <v-btn v-bind="attrs" v-on="on">
              {{ currentLangName }}
              <v-icon right role="img" aria-hidden="false">
                mdi-chevron-down
              </v-icon>
            </v-btn>
          </template>
          <list-languages
              :init-lang="extra.lang"
              @change-lang="changeLang"
          ></list-languages>
        </v-menu>
      </v-list-item>

    </v-list>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ListLanguages from '@/components/ListLanguages.vue';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import {UserExtra} from '@/packet/user';

@Component({
  components: {
    ToolbarBreadcrumbs,
    ListLanguages,
  }
})
export default class SelfAppearance extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Account',
      disabled: false,
      href: () => this.moveToSelf(),
    },
    {
      text: 'Appearance',
      disabled: true,
    },
  ];

  extra!: UserExtra;

  created() {
    this.extra = this.getInitExtra();
  }

  getInitExtra(): UserExtra {
    const userExtra = this.$localStore.user.extra;
    const result = {} as UserExtra;

    if (userExtra && userExtra.dark !== undefined) {
      result.dark = userExtra.dark;
    } else {
      result.dark = this.$vuetify.theme.dark;
    }

    if (userExtra && userExtra.lang !== undefined) {
      result.lang = userExtra.lang;
    } else {
      result.lang = this.$vuetify.lang.current;
    }
    return result;
  }

  get currentLangName(): string {
    const lang = this.extra.lang;
    if (!lang) {
      return '';
    }
    return this.$t('lang', lang).toString();
  }

  saveUserExtra() {
    this.$api2.patchSelfExtra(this.extra)
        .then(() => {
          console.debug('Upload user information to a remote server.');
        })
        .catch(error => {
          console.error(error);
        });
  }

  changeDark() {
    const dark = this.extra.dark;
    if (dark === undefined) {
      console.error('extra.dark is undefined error.');
      return;
    }

    // Local settings should not be changed.
    this.$vuetify.theme.dark = dark;
    this.$localStore.dark = dark;
    this.$localStore.userExtraDark = dark;

    this.saveUserExtra();
  }

  changeLang(lang: string) {
    this.extra.lang = lang;

    // Local settings should not be changed.
    this.$vuetify.lang.current = lang;
    this.$i18n.locale = lang;
    this.$localStore.lang = lang;
    this.$localStore.userExtraLang = lang;

    this.saveUserExtra();
  }
}
</script>