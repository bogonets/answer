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

            <v-card-text>
              <v-form v-if="isReady">
                <v-text-field
                    :label="$t('user_name')"
                    type="text"
                ></v-text-field>
                <v-text-field
                    :label="$t('password')"
                    type="password"
                    autocomplete="off"
                ></v-text-field>
              </v-form>
              <v-container v-else>
                <v-row class="my-12" align="center" justify="center">
                  <v-progress-linear
                      v-if="isInitializing"
                      color="primary"
                      height="6"
                      rounded
                      indeterminate
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

            <v-card-actions v-if="isReady" class="d-block">
              <v-list>
                <v-list-item>
                  <v-btn
                      rounded
                      block
                      color="primary"
                      :disabled="disabledSignin"
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
          @keydown.esc="onClickChangeApiCancel"
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
                @keypress.enter.stop="onClickChangeApiOk"
            ></v-text-field>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                text
                @click="onClickChangeApiCancel"
            >
              {{ $t('cancel') }}
            </v-btn>
            <v-btn
                color="primary"
                text
                @click="onClickChangeApiOk"
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

enum LoginPageState {
  Initializing,
  Unreachable,
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

  private currentState = LoginPageState.Initializing;
  private currentLangIndex = 0;
  private currentApiOrigin = "";
  private visibleApiSettingDialog = false;
  private disabledSignin = true;
  private visibleLoading = true;

  // onShift =  false;
  // onEnter =  false;
  // openSetting = false;
  // api_url = "";

  get isInitializing(): boolean {
    return this.currentState == LoginPageState.Initializing;
  }

  get isUnreachable(): boolean {
    return this.currentState == LoginPageState.Unreachable;
  }

  get isReady(): boolean {
    return this.currentState == LoginPageState.Ready;
  }

  get loadingText(): string {
    switch (this.currentState) {
      case LoginPageState.Initializing:
        return this.$t('connecting_api').toString()
      case LoginPageState.Unreachable:
        return this.$t('unreachable_api').toString()
      default:
        return "";
    }
  }

  mounted() {
    if (!this.$vuetify.lang.current) {
      this.$vuetify.lang.current = LANG_KO;
    }

    this.currentLangIndex = LANGUAGES.indexOf(this.$vuetify.lang.current);
    this.currentApiOrigin = this.$persist.apiOrigin;
    // this.$localStore.getters["etc/getApiUrl"];

    this.$api.setUrl(this.currentApiOrigin);
    this.$api2.origin = this.currentApiOrigin;

    if (this.isReady) {
      this.updateState(LoginPageState.Ready);
    } else {
      this.requestTestInit();
    }
  }

  private requestTestInit() {
    console.debug('Testing API ...');
    this.updateState(LoginPageState.Initializing);

    this.$api2.testInit()
        .then(response => {
          if (response.status == 200) {
            console.info('Initialized !!');
            this.updateState(LoginPageState.Ready);
          } else {
            console.warn('A reachable but uninitialized API.');
            this.$router.push("/signupadmin");
          }
        })
        .catch(error => {
          console.warn('Unreachable API.');
          this.updateState(LoginPageState.Unreachable);
        });
  }

  private updateState(s: LoginPageState): void {
    this.currentState = s;
    switch (s) {
      case LoginPageState.Initializing:
        this.disabledSignin = true;
        this.visibleLoading = true;
        break;

      case LoginPageState.Unreachable:
        this.disabledSignin = true;
        this.visibleLoading = false;
        break;

      case LoginPageState.Ready:
        this.disabledSignin = false;
        this.visibleLoading = false;
        break;
    }
  }

  onClickTheme() {
    this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
  }

  onClickTranslate(lang: string) {
    if (this.$vuetify.lang.current != lang) {
      this.$vuetify.lang.current = lang;
      this.$i18n.locale = lang;
      this.$store.commit("language/setLanguage", { language: lang });
    }
  }

  onClickChangeApiCancel() {
    this.visibleApiSettingDialog = false;
    this.currentApiOrigin = this.$persist.apiOrigin;
  }

  onClickChangeApiOk() {
    this.visibleApiSettingDialog = false;
    this.$persist.apiOrigin = this.currentApiOrigin
    this.$api.setUrl(this.currentApiOrigin);
    this.$api2.origin = this.currentApiOrigin;

    this.$nextTick(() => {
      this.requestTestInit();
    });
  }

  onClickSignin() {
  }

  onClickSignup() {
    this.$router.push('/signup');
  }

  onClickFindPassword() {
    // EMPTY.
  }

  //     initCheckLists: [
  //       {
  //         name: "checking_init_api",
  //         i18n: true,
  //         func: () => {
  //           return new Promise((resolve, reject) => {
  //             this.$api
  //               .checkAdmin()
  //               .then((res) => {
  //                 if (res.data.status === "ERROR") {
  //                   this.$info(
  //                     this.$options.name,
  //                     "API::checkAdmin",
  //                     "Is not existed admin."
  //                   );
  //                   setTimeout(() => {
  //                     reject({
  //                       status: true,
  //                       message:
  //                         "&nbsp;" +
  //                         this.$t("is_not_existed_admin_go_to_signup_admin"),
  //                     });
  //                   }, 1000);
  //                 } else {
  //                   setTimeout(() => {
  //                     resolve(true);
  //                   }, 1000);
  //                 }
  //               })
  //               .catch((err) => {
  //                 setTimeout(() => {
  //                   reject({ status: false, message: err });
  //                 }, 1000);
  //               });
  //           });
  //         },
  //         complete: false,
  //         status: null,
  //         onError: (e) => {
  //           if (e.status) {
  //             setTimeout(() => {
  //               this.$router.push("/signupadmin");
  //             }, 3000);
  //           } else {
  //             this.$error("API", "checkAdmin", e);
  //           }
  //         },
  //       },
  //     ],

  // onOpenApiSettingDialog() {
  //   this.api_url = this.$api.getUrl();
  //   this.openSetting = true;
  //   this.$nextTick().then(() => {
  //     this.$refs.apiUrl.focus();
  //   });
  // }

  // onCancel() {
  //   this.openSetting = false;
  // }

  // onOk() {
  //   this.$api.setUrl(this.api_url);
  //   this.$ls.setItem("etc/setApiUrl", { url: this.api_url });
  //   this.openSetting = false;
  //   this.initComplete = false;
  //   this.$nextTick(() => {
  //     if (!this.$refs.loader) {
  //       return;
  //     }
  //     this.$refs.loader.allRetry();
  //   });
  // }

  // get ok_disabled() {
  //   if (this.api_url === "") {
  //     return false;
  //   } else if (!this.api_url) {
  //     return false;
  //   }
  //   return true;
  // }
}
</script>

<style lang="scss" scoped>
//@import "~@/styles/sass/user-select-none.scss";

//.no-select {
//  @include user-select-none;
//}

//.container {
//  display: inline-block;
//  /* background-color: whitesmoke; */
//}

//.md-app {
//  border: 1px solid rgba(0, 0, 0, 0.12);
//}

//.content-style {
//  margin-top: 60px;
//  margin-bottom: auto;
//}

.config-button-group-position {
  position: absolute;
  top: 15px;
  right: 15px;
}
</style>
