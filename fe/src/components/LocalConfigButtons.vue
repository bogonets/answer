<template>
  <v-row justify="space-around">

    <!-- Theme Config Button -->
    <v-btn icon small @click="onClickTheme">
      <v-icon small role="img" aria-hidden="false">
        {{ icons.theme }}
      </v-icon>
    </v-btn>

    <!-- Language Config Button -->
    <menu-translate init-vuetify @select-lang="onClickLanguage"></menu-translate>

    <!-- API Config Button & Dialog -->
    <v-dialog
        v-if="!isProduction"
        v-model="showApiConfigDialog"
        max-width="800px"
        persistent
        no-click-animation
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
import MenuTranslate from '@/components/MenuTranslate.vue';
import { mdiThemeLightDark, mdiApi } from '@mdi/js';

export const EVENT_ON_CHANGE_THEME = 'on-change-theme';
export const EVENT_ON_CHANGE_LANGUAGE = 'on-change-language';
export const EVENT_ON_CHANGE_API = 'on-change-api';

@Component({
  components: {
    MenuTranslate
  }
})
export default class LocalConfigButtons extends Vue {

  readonly icons = {
    theme: mdiThemeLightDark,
    api: mdiApi,
  };

  private showApiConfigDialog = false;
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
    this.currentApiOrigin = this.$api2.origin;
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
