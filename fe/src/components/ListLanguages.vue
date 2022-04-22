<i18n lang="yaml">
en:
  lang: 'English'

ko:
  lang: '한글'
</i18n>

<template>
  <v-list :dense="dense">
    <v-subheader v-if="!!header">{{ header }}</v-subheader>
    <v-divider v-if="!!header"></v-divider>

    <v-list-item-group mandatory color="primary" :value="index" @change="changeLang">
      <v-list-item v-for="lang in languages" :key="lang">
        <v-list-item-content>
          <v-list-item-title v-text="$t('lang', lang)"></v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script lang="ts">
import VueI18n from '@/translations/VueI18n';
import {Component, Prop, Emit} from 'vue-property-decorator';

export const LANG_KO = 'ko';
export const LANG_EN = 'en';
export const LANGUAGES = [LANG_KO, LANG_EN];

@Component
export default class ListLanguages extends VueI18n {
  readonly languages = LANGUAGES;

  @Prop({type: Boolean, default: false})
  readonly dense!: boolean;

  @Prop({type: String, default: ''})
  readonly header!: string;

  @Prop({type: String, default: ''})
  readonly initLang!: string;

  @Prop({type: Boolean, default: false})
  readonly initVuetify!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initLocalStore!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initUserExtra!: boolean;

  index = 0;

  created() {
    this.index = LANGUAGES.indexOf(this.getInitLang());
  }

  getInitLang() {
    if (this.initLang) {
      return this.initLang;
    } else if (this.initVuetify) {
      return this.$vuetify.lang.current;
    } else if (this.initLocalStore) {
      return this.$localStore.lang;
    } else if (this.initUserExtra) {
      if (this.$localStore.user.extra && this.$localStore.user.extra.lang) {
        return this.$localStore.user.extra.lang;
      }
    }

    // Default settings.
    if (this.$vuetify.lang.current) {
      return this.$vuetify.lang.current;
    } else {
      return LANG_KO;
    }
  }

  @Emit()
  changeLang(index: number) {
    this.index = index;
    return LANGUAGES[index];
  }
}
</script>
