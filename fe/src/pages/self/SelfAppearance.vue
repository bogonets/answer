<i18n lang="yaml">
en:
  lang: 'English'
  title: 'Appearance'
  subtitle: 'Customize the look and feel of your Answer.'
  headers:
    timezone: 'Timezone'
  subheaders:
    timezone: 'By setting the time zone, you can change the time format.'
  theme:
    header: 'Theme'
    dark:
      title: 'Dark Mode'
      subtitle: 'Apply a theme that displays white text on a dark screen.'
  i18n:
    header: 'Internationalization'
    lang:
      title: 'Language'
      subtitle: 'It will be translated into your preferred language.'

ko:
  lang: '한글'
  title: '외관 설정'
  subtitle: 'Answer의 모양과 느낌을 설정할 수 있습니다.'
  headers:
    timezone: '시간대'
  subheaders:
    timezone: '시간대를 설정하여, 출력 포맷을 변경할 수 있습니다.'
  theme:
    header: '테마'
    dark:
      title: '어두운 화면'
      subtitle: '어두운 화면에 흰 글자를 나타내는 테마를 적용합니다.'
  i18n:
    header: '국제화'
    lang:
      title: '언어'
      subtitle: '원하는 언어로 번역됩니다.'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-subheader>{{ $t('theme.header') }}</v-subheader>
    <left-title
      x-small
      no-gutter
      no-wrap-xs
      :left-ratio="8"
      :right-ratio="4"
      :header="$t('theme.dark.title')"
      :subheader="$t('theme.dark.subtitle')"
    >
      <div class="d-flex flex-row justify-end">
        <v-switch inset v-model="dark" @change="onChangeDark"></v-switch>
      </div>
    </left-title>

    <v-divider></v-divider>
    <v-subheader>{{ $t('i18n.header') }}</v-subheader>

    <left-title
      x-small
      no-gutter
      no-wrap-xs
      :left-ratio="8"
      :right-ratio="4"
      :header="$t('i18n.lang.title')"
      :subheader="$t('i18n.lang.subtitle')"
    >
      <div class="d-flex flex-row justify-end">
        <v-menu transition="slide-y-transition" :offset-y="true">
          <template v-slot:activator="{on, attrs}">
            <v-btn v-bind="attrs" v-on="on">
              {{ currentLangName }}
              <v-icon right role="img" aria-hidden="false">mdi-chevron-down</v-icon>
            </v-btn>
          </template>
          <list-languages
            :init-lang="lang"
            @change-lang="onChangeLang"
          ></list-languages>
        </v-menu>
      </div>
    </left-title>

    <left-title
      x-small
      no-gutter
      no-wrap-xs
      :left-ratio="8"
      :right-ratio="4"
      :header="$t('headers.timezone')"
      :subheader="$t('subheaders.timezone')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
          dense
          outlined
          hide-details
          v-model="timezone"
          :items="timezoneNames"
          @change="onChangeTimezone"
        ></v-combobox>
      </div>
    </left-title>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import ListLanguages from '@/components/ListLanguages.vue';
import type {UpdateUserQ} from '@recc/api/dist/packet/user';
import momentTimezone from 'moment-timezone';
import moment from 'moment-timezone';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    ListLanguages,
  },
})
export default class SelfAppearance extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Self',
      disabled: false,
      href: () => this.moveToSelf(),
    },
    {
      text: 'Appearance',
      disabled: true,
    },
  ];

  private readonly timezoneNames = momentTimezone.tz.names();

  loading = false;
  dark = 0;
  lang = '';
  timezone = '';

  created() {
    this.dark = this.$localStore.userDark;
    this.lang = this.$localStore.userLang;
    this.timezone = this.$localStore.userTimezone;
  }

  get currentLangName(): string {
    const lang = this.lang;
    if (!lang) {
      return '';
    }
    return this.$t('lang', lang).toString();
  }

  saveUserExtra(data: UpdateUserQ) {
    this.loading = true;
    this.$api2
      .patchSelf(data)
      .then(() => {
        this.loading = false;
        this.toastRequestSuccess();
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onChangeDark() {
    // Local settings should not be changed.
    this.$vuetify.theme.dark = !!this.dark;
    this.$localStore.dark = !!this.dark;
    this.$localStore.userDark = this.dark;

    this.saveUserExtra({dark: this.dark});
  }

  onChangeLang(lang: string) {
    // Local settings should not be changed.
    this.$vuetify.lang.current = this.lang;
    this.$i18n.locale = this.lang;
    this.$localStore.lang = this.lang;
    this.$localStore.userLang = this.lang;
    moment.locale(lang);

    this.saveUserExtra({lang: this.lang});
  }

  onChangeTimezone(timezone: string) {
    // Local settings should not be changed.
    momentTimezone.tz.setDefault(this.timezone);
    this.$localStore.timezone = this.timezone;
    this.$localStore.userTimezone = this.timezone;

    this.saveUserExtra({timezone: this.timezone});
  }
}
</script>
