<template>
  <v-main>

    <!-- The card in the center of the screen. -->
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col cols="8" sm="6" md="6" lg="6" xl="4">
          <v-card>

            <v-card-title>
              <title-logo class="mt-4"></title-logo>
            </v-card-title>

            <v-fade-transition hide-on-leave>
              <v-card-text v-if="!isReady">
                <linear-loading
                    :progress-color="progressColor"
                    :progress-indeterminate="isConnecting"
                    :loading-text="loadingText"
                ></linear-loading>
              </v-card-text>
            </v-fade-transition>

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

            <v-card-actions v-if="isReady" class="d-block">
              <v-list>
                <v-list-item>
                  <v-btn
                      rounded
                      block
                      color="primary"
                      :loading="showLoading"
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
      </v-row>
    </v-container>

    <local-config-buttons
        class="config-button-group-position ma-0 pa-0"
        @on-change-theme="onChangeTheme"
        @on-change-language="onChangeLanguage"
        @on-change-api="onChangeApi"
    ></local-config-buttons>

  </v-main>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import TitleLogo from '@/components/Title/TitleLogo.vue';
import LinearLoading from '@/components/Progress/LinearLoading.vue';
import LocalConfigButtons from '@/components/Config/LocalConfigButtons.vue';

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
    LocalConfigButtons,
    LinearLoading,
    TitleLogo,
  }
})
export default class Login extends Vue {

  private readonly waitMoment = WAIT_MOMENT_MILLISECONDS;

  private currentUserName = '';
  private currentUserPassword = '';
  private currentState = LoginPageState.Connecting;
  private showLoading = false;

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
        return '';
      default:
        return '';
    }
  }

  get progressColor(): string {
    switch (this.currentState) {
      case LoginPageState.Connecting:
        return 'primary';
      case LoginPageState.Unreachable:
        return 'error';
      case LoginPageState.Uninitialized:
        return 'error';
      case LoginPageState.ReadyForWait:
        return 'primary';
      case LoginPageState.Ready:
        return 'primary';
      default:
        return 'primary';
    }
  }

  private saveLoginToken(access: string, refresh: string) {
    this.$store.commit('user/login', {
      accessToken: access,
      refreshToken: refresh,
      id: '',
      email: '',
      phone: '',
    });
  }

  private saveLanguage(lang: string): void {
    this.$localStore.commit('language/setLanguage', lang);
  }

  private saveDarkTheme(dark: boolean): void {
    this.$localStore.commit('theme/setTheme', dark);
  }

  private saveApiOrigin(origin: string): void {
    this.$localStore.commit('etc/setApiUrl', origin);
  }

  mounted() {
    if (this.isReady) {
      this.updateState(LoginPageState.Ready);
    } else {
      this.testInit();
    }
  }

  private testInit() {
    this.updateState(LoginPageState.Connecting);

    this.$api2.testInit()
        .then(response => {
          this.updateState(LoginPageState.ReadyForWait);
          setTimeout(() => {
            this.updateState(LoginPageState.Ready);
          }, this.waitMoment);
        })
        .catch(error => {
          if (error.response) {
            if (error.response.status && error.response.status == 520) {
              this.$router.push('/signupadmin');
            } else {
              this.updateState(LoginPageState.Unreachable);
            }
          } else {
            this.updateState(LoginPageState.Unreachable);
          }
        });
  }

  private updateState(state: LoginPageState): void {
    const oldVal = LoginPageState[this.currentState];
    const newVal = LoginPageState[state];
    this.currentState = state;
    console.debug(`Change login page state: ${oldVal} -> ${newVal}`);
  }

  onChangeTheme(dark: boolean) {
    const themeText = dark ? 'Dark' : 'Light';
    console.debug('Change Theme: ' + themeText);
    this.saveDarkTheme(dark);
  }

  onChangeLanguage(lang: string) {
    console.debug('Change Language: ' + lang);
    this.saveLanguage(lang);
  }

  onChangeApi(origin: string) {
    console.debug('Change API origin: ' + origin);
    this.saveApiOrigin(origin);
    this.testInit();
  }

  onClickSignin() {
    this.showLoading = true;

    this.$api2.login(this.currentUserName, this.currentUserPassword)
        .then(response => {
          this.showLoading = false;
          const access = response.access ? response.access : '';
          const refresh = response.refresh ? response.refresh : '';
          console.debug('Login successful !!');
          this.saveLoginToken(access, refresh)
          this.$router.push('/main');
        })
        .catch(error => {
          this.showLoading = false;
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
