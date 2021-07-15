<template>
  <v-main>
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col cols="8" sm="6" md="6" lg="4" xl="2">
          <v-card>

            <v-card-title>
              <v-container>
                <v-row align="center" justify="center">
                  <title-logo
                      class="align-self-center mx-auto my-6"
                      :is-text-mode="false"
                      :is-uppercase="false"
                      :text="'answer'"
                  ></title-logo>
                </v-row>
              </v-container>
            </v-card-title>

            <v-expand-transition>
              <v-card-text v-if="isReady">
                <v-form>
                  <v-text-field
                      type="text"
                      v-model="currentUserName"
                      :label="$t('user_name')"
                  ></v-text-field>
                  <v-text-field
                      type="password"
                      autocomplete="off"
                      v-model="currentUserPassword"
                      :label="$t('password')"
                  ></v-text-field>
                </v-form>
              </v-card-text>
            </v-expand-transition>

            <v-fade-transition>
              <v-card-text v-if="!isReady">
                <v-container>
                  <v-row class="my-12" align="center" justify="center">
                    <v-progress-linear
                        v-if="isConnecting"
                        color="primary"
                        height="6"
                        rounded
                        indeterminate
                    ></v-progress-linear>
                    <v-progress-linear
                        v-if="isReadyForWait"
                        color="primary"
                        height="6"
                        rounded
                    ></v-progress-linear>
                    <v-progress-linear
                        v-else-if="isUnreachable"
                        color="error"
                        height="6"
                        rounded
                    ></v-progress-linear>
                  </v-row>
                  <v-row class="my-6" align="center" justify="center">
                    {{ loadingText }}
                  </v-row>
                </v-container>
              </v-card-text>
            </v-fade-transition>

            <v-card-actions v-if="isReady" class="d-block">
              <v-list>
                <v-list-item>
                  <v-btn
                      rounded
                      block
                      color="primary"
                      :loading="visibleLoading"
                      @click="onClickSignin"
                  >
                    {{ $t('sign_in') }}
                  </v-btn>
                </v-list-item>
                <v-divider class="mt-4 pt-4"></v-divider>
                <v-list-item>
                  <v-row align="center" justify="center">
                    <v-spacer></v-spacer>
                    <a
                        class="text-overline"
                        @click="onClickSignup"
                    >
                      {{ $t('sign_up') }}
                    </a>
                    <span class="mx-3"></span>
                    <a
                        class="text-overline text--disabled text-decoration-line-through"
                        @click="onClickFindPassword"
                    >
                      {{ $t('forgot_password') }}
                    </a>
                    <v-spacer></v-spacer>
                  </v-row>
                </v-list-item>
              </v-list>
            </v-card-actions>

          </v-card>
        </v-col>

<!--              <v-expand-transition hide-on-leave>-->
<!--        <af-login-form v-if="initComplete"></af-login-form>-->
<!--              </v-expand-transition>-->
<!--              <v-fade-transition hide-on-leave>-->
<!--                <v-card-text v-if="!initComplete">-->
<!--                  <v-loader-->
<!--                      :serialize="false"-->
<!--                      :loadList="initCheckLists"-->
<!--                      @allComplete="initComplete = $event"-->
<!--                      ref="loader"-->
<!--                  ></v-loader>-->
<!--                </v-card-text>-->
<!--              </v-fade-transition>-->
<!--            </v-card>-->
<!--          </v-flex>-->
      </v-row>

    </v-container>

    <v-row class="config-button-group-position ma-0 pa-0" justify="space-around">
      <v-btn
          icon
          small
          @click="onClickTheme"
      >
        <v-icon
            small
            role="img"
            aria-hidden="false"
        >
          {{ icons.theme }}
        </v-icon>
      </v-btn>

      <v-menu
          open-on-hover
          transition="slide-y-transition"
          :offset-y="true"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              icon
              small
              v-bind="attrs"
              v-on="on"
          >
            <v-icon
                small
                role="img"
                aria-hidden="false"
            >
              {{ icons.translate }}
            </v-icon>
          </v-btn>
        </template>

        <v-list dense>
          <v-subheader>{{ $t('translations') }}</v-subheader>
          <v-divider></v-divider>
          <v-list-item-group
              mandatory
              v-model="currentLangIndex"
              color="primary"
          >
            <v-list-item
                v-for="lang in languages"
                :key="lang"
            >
              <v-list-item-content @click="onClickTranslate(lang)">
                <v-list-item-title v-text="$t(lang)"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>

      <v-dialog
          v-model="visibleApiSettingDialog"
          persistent
          @keydown.esc="onApiDialogCancel"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              icon
              small
              v-bind="attrs"
              v-on="on"
          >
            <v-icon small role="img" aria-hidden="false">{{icons.api}}</v-icon>
          </v-btn>
        </template>

        <v-card>
          <v-card-title>
            <span>{{ $t('api_settings') }}</span>
          </v-card-title>

          <v-card-subtitle class="mt-1">
            <span>{{ $t('api_change_origin') }}</span>
          </v-card-subtitle>

          <v-card-text>
            <v-text-field
                required
                v-model="currentApiOrigin"
                :label="$t('api_origin')"
                @keypress.enter.stop="onApiDialogOk"
            ></v-text-field>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                text
                @click="onApiDialogCancel"
            >
              {{ $t('cancel') }}
            </v-btn>
            <v-btn
                color="primary"
                text
                @click="onApiDialogOk"
            >
              {{ $t('ok') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </v-row>

<!--    <v-dialog-->
<!--      v-model="openSetting"-->
<!--      max-width="500px"-->
<!--      scrollable-->
<!--      transition="dialog-transition"-->
<!--      :overlay="false"-->
<!--      :dark="$vuetify.theme.dark"-->
<!--    >-->
<!--      <v-card outlined>-->
<!--        <v-card-title>-->
<!--          <span>API Configure</span>-->
<!--        </v-card-title>-->
<!--        <v-divider></v-divider>-->
<!--        <v-card-text class="pa-4">-->
<!--          <v-text-field-->
<!--            dense-->
<!--            outlined-->
<!--            hide-details-->
<!--            ref="apiUrl"-->
<!--            label="API Address"-->
<!--            v-model="api_url"-->
<!--            clearable-->
<!--            @keypress.enter.stop="onOk"-->
<!--          ></v-text-field>-->
<!--        </v-card-text>-->
<!--        <v-divider></v-divider>-->
<!--        <v-card-actions>-->
<!--          <v-btn @click="onCancel">{{ $t("cancel") }}</v-btn>-->
<!--          <v-spacer></v-spacer>-->
<!--          <v-btn @click="onOk" :disabled="!ok_disabled">{{ $t("ok") }}</v-btn>-->
<!--        </v-card-actions>-->
<!--      </v-card>-->
<!--    </v-dialog>-->
  </v-main>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { mdiApi, mdiTranslate, mdiThemeLightDark } from '@mdi/js';
import TitleLogo from '@/components/Title/TitleLogo.vue';

const LANG_KO = 'ko';
const LANG_EN = 'en';
const LANGUAGES = [LANG_KO, LANG_EN];

const WAIT_MOMENT_MILLISECONDS = 1000;

enum LoginPageState {
  Connecting,
  Unreachable,
  Uninitialized,
  ReadyForWait,
  Ready,
}

@Component({
  components: {
    TitleLogo,
  }
})
export default class Login extends Vue {

  private readonly languages = LANGUAGES;
  private readonly icons = {
    api: mdiApi,
    translate: mdiTranslate,
    theme: mdiThemeLightDark,
  };

  private readonly waitMoment = WAIT_MOMENT_MILLISECONDS;

  private currentUserName = "";
  private currentUserPassword = "";
  private currentState = LoginPageState.Connecting;
  private currentLangIndex = 0;
  private currentApiOrigin = "";

  private visibleApiSettingDialog = false;
  private visibleLoading = false;

  get isConnecting(): boolean {
    return this.currentState == LoginPageState.Connecting;
  }

  get isUnreachable(): boolean {
    return this.currentState == LoginPageState.Unreachable;
  }

  get isUninitialized(): boolean {
    return this.currentState == LoginPageState.Uninitialized;
  }

  get isReadyForWait(): boolean {
    return this.currentState == LoginPageState.ReadyForWait;
  }

  get isReady(): boolean {
    return this.currentState == LoginPageState.Ready;
  }

  get loadingText(): string {
    switch (this.currentState) {
      case LoginPageState.Connecting:
        return this.$t('connecting_api').toString()
      case LoginPageState.Unreachable:
        return this.$t('unreachable_api').toString()
      case LoginPageState.Uninitialized:
        return this.$t('uninitialized_api').toString()
      case LoginPageState.ReadyForWait:
        return this.$t('connected_api').toString()
      case LoginPageState.Ready:
        return "";
      default:
        return "";
    }
  }

  private saveLanguage(lang: string) {
    this.$store.commit('language/setLanguage', { language: lang });
  }

  private saveLoginToken(access: string, refresh: string) {
    this.$store.commit("user/login", {
      accessToken: access,
      refreshToken: refresh,
      id: "",
      email: "",
      phone: "",
    });
  }

  private saveApiOrigin(origin: string) {
    this.$localStore.commit('etc/setApiUrl', { url: origin });
  }

  private loadApiOrigin(): string {
    return this.$localStore.getters['etc/getApiUrl'];
  }

  mounted() {
    if (!this.$vuetify.lang.current) {
      this.$vuetify.lang.current = LANG_KO;
    }

    this.currentLangIndex = LANGUAGES.indexOf(this.$vuetify.lang.current);
    this.currentApiOrigin = this.loadApiOrigin();
    this.$api.setUrl(this.currentApiOrigin);
    this.$api2.origin = this.currentApiOrigin;

    if (this.isReady) {
      this.updateState(LoginPageState.Ready);
    } else {
      this.requestTestInit();
    }
  }

  private requestTestInit() {
    this.updateState(LoginPageState.Connecting);

    this.$api2.testInit()
        .then(response => {
          if (response.status == 200) {
            this.updateState(LoginPageState.ReadyForWait);
            setTimeout(() => {
              this.updateState(LoginPageState.Ready);
            }, this.waitMoment);
          } else {
            this.updateState(LoginPageState.Unreachable);
            setTimeout(() => {
              this.$router.push('/signupadmin');
            }, this.waitMoment);
          }
        })
        .catch(error => {
          this.updateState(LoginPageState.Unreachable);
        });
  }

  private updateState(s: LoginPageState): void {
    this.currentState = s;
  }

  onClickTheme() {
    this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
  }

  onClickTranslate(lang: string) {
    if (this.$vuetify.lang.current != lang) {
      this.$vuetify.lang.current = lang;
      this.$i18n.locale = lang;
      this.saveLanguage(lang);
    }
  }

  onApiDialogCancel() {
    this.visibleApiSettingDialog = false;
    this.currentApiOrigin = this.loadApiOrigin();
  }

  onApiDialogOk() {
    this.visibleApiSettingDialog = false;
    this.saveApiOrigin(this.currentApiOrigin);
    this.$api.setUrl(this.currentApiOrigin);
    this.$api2.origin = this.currentApiOrigin;

    this.$nextTick(() => {
      this.requestTestInit();
    });
  }

  onClickSignin() {
    this.visibleLoading = true;

    this.$api2.login(this.currentUserName, this.currentUserPassword)
        .then(response => {
          this.visibleLoading = false;
          const access = response.access ? response.access : "";
          const refresh = response.refresh ? response.refresh : "";
          console.info('Login successful !!');
          this.saveLoginToken(access, refresh)
          this.$router.push('/main');
        })
        .catch(error => {
          this.visibleLoading = false;
          console.error(error);
        });
  }

  onClickSignup() {
    this.$router.push('/signup');
  }

  onClickFindPassword() {
    // EMPTY.
  }
}
</script>

<style lang="scss" scoped>
.config-button-group-position {
  position: absolute;
  top: 16px;
  right: 16px;
}
</style>
