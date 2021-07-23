<i18n lang="yaml">
en:
  dialog:
    api_config:
      title: "API Settings"
      subtitle: "You can change the API origin address."
      origin_label: "API origin address"
      cancel: "Cancel"
      ok: "Ok"

ko:
  dialog:
    api_config:
      title: "API 설정"
      subtitle: "서버 주소를 변경할 수 있습니다."
      origin_label: "API 서버 주소"
      cancel: "취소"
      ok: "확인"
</i18n>

<template>
  <v-row justify="space-around">

    <!-- Theme Config Button -->
    <v-btn icon small @click="changeTheme">
      <v-icon small role="img" aria-hidden="false">
        {{ icons.theme }}
      </v-icon>
    </v-btn>

    <!-- Language Config Button -->
    <menu-translate
        init-vuetify @input="changeLanguage"
    ></menu-translate>

    <!-- API Config Button & Dialog -->
    <v-dialog
        v-if="!isProduction"
        v-model="showApiConfigDialog"
        max-width="800px"
        persistent
        no-click-animation
        @keydown.esc.stop="cancelOrigin"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon small v-bind="attrs" v-on="on">
          <v-icon small role="img" aria-hidden="false">{{ icons.api }}</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title>
          <span>{{ $t('dialog.api_config.title') }}</span>
        </v-card-title>

        <v-card-subtitle class="mt-1">
          <span>{{ $t('dialog.api_config.subtitle') }}</span>
        </v-card-subtitle>

        <v-card-text>
          <v-text-field
              required
              v-model="currentApiOrigin"
              :label="$t('dialog.api_config.origin_label')"
              @keypress.enter.stop="changeOrigin"
          ></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="cancelOrigin">
            {{ $t('dialog.api_config.cancel') }}
          </v-btn>
          <v-btn color="primary" text @click="changeOrigin">
            {{ $t('dialog.api_config.ok') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-row>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit } from 'vue-property-decorator';
import MenuTranslate from '@/components/MenuTranslate.vue';
import { mdiThemeLightDark, mdiApi } from '@mdi/js';

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

  @Prop({type: String, default: ''})
  readonly origin!: string;

  @Prop({type: Boolean, default: false})
  readonly localStoreOrigin!: boolean;

  @Prop({type: Boolean, default: false})
  readonly apiOrigin!: boolean;

  @Prop({type: Boolean, default: false})
  readonly locationOrigin!: boolean;

  private showApiConfigDialog = false;
  private savedApiOrigin = '';
  private currentApiOrigin = '';

  created() {
    this.savedApiOrigin = this.getInitApiOrigin();
    this.currentApiOrigin = this.savedApiOrigin;
  }

  get isProduction(): boolean {
    return process.env.NODE_ENV === 'production';
  }

  private getInitApiOrigin(): string {
    if (this.origin) {
      return this.origin;
    } else if (this.localStoreOrigin) {
      return this.$localStore.origin;  // Perhaps the default is location origin.
    } else if (this.apiOrigin) {
      return this.$api2.origin;
    } else if (this.locationOrigin) {
      return document.location.origin;
    }

    // Default settings.
    const localStoreOrigin = this.$localStore.origin;
    if (localStoreOrigin) {
      return localStoreOrigin;
    } else {
      return document.location.origin;
    }
  }

  @Emit()
  changeTheme() {
    return !this.$vuetify.theme.dark;
  }

  @Emit()
  changeLanguage(lang: string) {
    return lang;
  }

  @Emit()
  cancelOrigin() {
    this.showApiConfigDialog = false;
    this.currentApiOrigin = this.savedApiOrigin;
    return this.savedApiOrigin;
  }

  @Emit()
  changeOrigin() {
    this.showApiConfigDialog = false;
    this.savedApiOrigin = this.currentApiOrigin;
    return this.currentApiOrigin;
  }
}
</script>
