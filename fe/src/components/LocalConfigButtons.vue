<template>
  <v-row justify="space-around">

    <!-- Theme Config Button -->
    <v-btn icon small @click="onClickTheme">
      <v-icon small role="img" aria-hidden="false">
        {{ icons.theme }}
      </v-icon>
    </v-btn>

    <!-- Language Config Button -->
    <v-menu open-on-hover transition="slide-y-transition" :offset-y="true">
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon small v-bind="attrs" v-on="on">
          <v-icon small role="img" aria-hidden="false">
            {{ icons.translate }}
          </v-icon>
        </v-btn>
      </template>

      <v-list dense>
        <v-subheader>{{ $t('config.translations.title') }}</v-subheader>
        <v-divider></v-divider>

        <v-list-item-group mandatory v-model="currentLangIndex" color="primary">
          <v-list-item v-for="lang in languages" :key="lang">
            <v-list-item-content @click="onClickLanguage(lang)">
              <v-list-item-title v-text="$t(lang)"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-menu>

    <!-- API Config Button & Dialog -->
    <v-dialog
        v-if="!isProduction"
        v-model="showApiConfigDialog"
        persistent
        @keydown.esc.stop="onApiDialogCancel"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon small v-bind="attrs" v-on="on">
          <v-icon small role="img" aria-hidden="false">{{ icons.api }}</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title>
          <span>{{ $t('config.api.title') }}</span>
        </v-card-title>

        <v-card-subtitle class="mt-1">
          <span>{{ $t('config.api.subtitle') }}</span>
        </v-card-subtitle>

        <v-card-text>
          <v-text-field
              required
              v-model="currentApiOrigin"
              :label="$t('config.api.origin_address')"
              @keypress.enter.stop="onApiDialogOk"
          ></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="onApiDialogCancel">
            {{ $t('basic.cancel') }}
          </v-btn>
          <v-btn color="primary" text @click="onApiDialogOk">
            {{ $t('basic.ok') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { mdiThemeLightDark, mdiTranslate, mdiApi } from '@mdi/js';

export const LANG_KO = 'ko';
export const LANG_EN = 'en';
export const LANGUAGES = [LANG_KO, LANG_EN];

export const EVENT_ON_CHANGE_THEME = 'on-change-theme';
export const EVENT_ON_CHANGE_LANGUAGE = 'on-change-language';
export const EVENT_ON_CHANGE_API = 'on-change-api';

@Component
export default class LocalConfigButtons extends Vue {

  readonly languages = LANGUAGES;
  readonly icons = {
    theme: mdiThemeLightDark,
    translate: mdiTranslate,
    api: mdiApi,
  };

  private showApiConfigDialog = false;
  private currentLangIndex = 0;
  private currentApiOrigin = '';

  // Lifecycle

  mounted() {
    this.updateInternalState();
  }

  // Computed

  get isProduction(): boolean {
    return process.env.NODE_ENV === 'production';
  }

  // Methods

  updateInternalState() {
    const lang = this.$vuetify.lang.current ? this.$vuetify.lang.current : LANG_KO;
    const api = this.$api2.origin;
    this.currentLangIndex = LANGUAGES.indexOf(lang);
    this.currentApiOrigin = api;
  }

  // Events

  onClickTheme() {
    // Flip light/dark theme.
    const dark = !this.$vuetify.theme.dark;
    this.$vuetify.theme.dark = dark;
    this.$emit(EVENT_ON_CHANGE_THEME, dark);
  }

  onClickLanguage(lang: string) {
    if (this.$vuetify.lang.current == lang) {
      return;
    }

    this.$vuetify.lang.current = lang;
    this.$i18n.locale = lang;
    this.$emit(EVENT_ON_CHANGE_LANGUAGE, lang);
  }

  onApiDialogCancel() {
    this.showApiConfigDialog = false;
    this.currentApiOrigin = this.$api2.origin;
  }

  onApiDialogOk() {
    this.showApiConfigDialog = false;
    if (this.currentApiOrigin == this.$api2.origin) {
      return;
    }

    const api = this.currentApiOrigin;
    this.$api.setUrl(api);
    this.$api2.origin = api;
    this.$emit(EVENT_ON_CHANGE_API, api);
  }
}
</script>
