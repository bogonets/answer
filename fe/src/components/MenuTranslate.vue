<i18n lang="yaml">
en:
  name: "English"
  header: "Translations"

ko:
  name: "한국어"
  header: "언어선택"
</i18n>

<template>
  <v-menu open-on-hover transition="slide-y-transition" :offset-y="true">

    <template v-slot:activator="{ on, attrs }"> <v-btn icon small v-bind="attrs" v-on="on">
        <v-icon small role="img" aria-hidden="false">
          {{ icons.translate }}
        </v-icon>
      </v-btn>
    </template>

    <v-list dense>
      <v-subheader>{{ $t('header') }}</v-subheader>
      <v-divider></v-divider>

      <v-list-item-group
          mandatory
          color="primary"
          :value="currentLangIndex"
          @change="changeLangIndex"
      >
        <v-list-item v-for="lang in languages" :key="lang">
          <v-list-item-content>
            <v-list-item-title v-text="$t('name', lang)"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>

  </v-menu>
</template>

<script lang="ts">
import { Vue, Component, Prop, VModel } from 'vue-property-decorator';
import { mdiTranslate } from "@mdi/js";

export const LANG_KO = 'ko';
export const LANG_EN = 'en';
export const LANGUAGES = [LANG_KO, LANG_EN];

@Component
export default class MenuTranslate extends Vue {

  readonly languages = LANGUAGES;
  readonly icons = {
    translate: mdiTranslate,
  };

  @VModel({ type: String })
  lang!: string;

  @Prop({type: Boolean, default: false})
  readonly initVuetify!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initLocalStore!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initUserExtra!: boolean;

  private currentLangIndex = 0;

  created() {
    const initValue = this.getInitLang();
    if (this.lang !== initValue) {
      this.lang = initValue;
    }
    this.currentLangIndex = LANGUAGES.indexOf(initValue);
  }

  private getInitLang(): string {
    if (this.lang) {
      return this.lang;
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

  changeLangIndex(index) {
    this.currentLangIndex = index;
    this.lang = LANGUAGES[index];
  }
}
</script>
