<i18n lang="yaml">
en:
  username: "Username"
  password: "Password"
  signin: "Sign in"
  signup: "Sign up"
  forgot_password: "Forgot password"
  msg:
    connecting_api: "Connecting to API server..."
    unreachable_api: "Unreachable API server."
    uninitialized_api: "A reachable but uninitialized API."
    connected_api: "API connection successful."
    required_field: "Required field"
    more_than_4char: "It must be at least 4 characters long."
    invalid_fields: "Invalid ID or password."

ko:
  username: "계정명"
  password: "비밀번호"
  signin: "로그인"
  signup: "회원 가입"
  forgot_password: "비밀번호 찾기"
  msg:
    connecting_api: "API 서버 연결중 ..."
    unreachable_api: "API 서버 연결에 실패하였습니다."
    uninitialized_api: "API 서버가 연결되었지만, 초기화되지 않았습니다."
    connected_api: "API 연결 설공."
    required_field: "공백을 허용하지 않습니다."
    more_than_4char: "4자 이상이여야 합니다."
    invalid_fields: "계정이름 또는 비밀번호가 잘못되었습니다."
</i18n>

<template>
  <v-main>

    <!-- The card in the center of the screen. -->
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col cols="8" sm="6" md="6" lg="6" xl="4">
          <v-card elevation="8">

            <v-card-title class="pt-8">
              <title-logo></title-logo>
            </v-card-title>

            <v-expand-transition>
              <v-row
                  v-if="isErrorMessage"
                  class="d-block mt-8 mb-4 mx-4"
                  align="center"
                  justify="center"
              >
                <v-alert dense outlined type="error">{{ errorMessage }}</v-alert>
              </v-row>
            </v-expand-transition>

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
                      ref="usernameField"
                      v-model="currentUsername"
                      :rules="[rules.username.required]"
                      :label="usernameFieldLabel"
                  ></v-text-field>
                  <v-text-field
                      type="password"
                      autocomplete="off"
                      ref="passwordField"
                      v-model="currentPassword"
                      :rules="[rules.password.required]"
                      :label="passwordFieldLabel"
                      @keypress.enter.stop="onClickSignin"
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
                    {{ $t('signin') }}
                  </v-btn>
                </v-list-item>

                <v-divider class="mt-4 pt-4"></v-divider>
                <v-list-item>
                  <v-row align="center" justify="center">
                    <v-spacer></v-spacer>
                    <a class="text-overline" @click="onClickSignup">
                      {{ $t('signup') }}
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
import { User } from '@/apis/api-v2';
import TitleLogo from '@/components/TitleLogo.vue';
import LinearLoading from '@/components/LinearLoading.vue';
import LocalConfigButtons from '@/components/LocalConfigButtons.vue';

const WAIT_MOMENT_MILLISECONDS = 0;
const V_TEXT_FIELD_VALIDATE_METHOD_NAME = 'validate';

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
export default class LoginPage extends Vue {

  private readonly waitMoment = WAIT_MOMENT_MILLISECONDS;
  private readonly rules = {
    username: {
      required: (value) => {
        return !!value || this.$t('msg.required_field');
      },
    },
    password: {
      required: (value) => {
        return !!value || this.$t('msg.required_field');
      },
    },
  };

  private currentUsername = '';
  private currentPassword = '';
  private currentState = LoginPageState.Connecting;
  private showLoading = false;
  private errorMessage = '';

  // Lifecycle

  mounted() {
    const access = this.$localStore.access;
    const refresh = this.$localStore.refresh;
    const user = this.$localStore.user;

    // Already session information?
    if (!!access && !!refresh && !!user) {
      console.info(`Already session information: ${user.username}`)

      this.saveUserToSession(access, refresh, user);
      this.moveToMainPage();

      this.$api.setDefaultSession(access, refresh, user);
      this.$api.setDefaultBearerAuthorization(access);

      return;
    }

    if (!this.isReady) {
      this.testInit();
    }
  }

  // Computed

  get usernameFieldLabel(): string {
    return this.$t('username').toString();
  }

  get passwordFieldLabel(): string {
    return this.$t('password').toString();
  }

  get isErrorMessage(): boolean {
    return !!this.errorMessage;
  }

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
        return this.$t('msg.connecting_api').toString()
      case LoginPageState.Unreachable:
        return this.$t('msg.unreachable_api').toString()
      case LoginPageState.Uninitialized:
        return this.$t('msg.uninitialized_api').toString()
      case LoginPageState.ReadyForWait:
        return this.$t('msg.connected_api').toString()
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

  // Methods

  saveUserToLocal(access: string, refresh: string, user: User) {
    this.$localStore.access = access;
    this.$localStore.refresh = refresh;
    this.$localStore.user = user;
  }

  saveUserToSession(access: string, refresh: string, user: User) {
    const username = user.username || '';
    const email = user.email || '';
    const phone = user.phone1 || '';

    this.$store.commit('user/login', {
      accessToken: access,
      refreshToken: refresh,
      id: username,
      email: email,
      phone: phone,
    });
  }

  saveLanguage(lang: string): void {
    this.$localStore.lang = lang;
  }

  saveDarkTheme(dark: boolean): void {
    this.$localStore.dark = dark;
  }

  saveApiOrigin(origin: string): void {
    this.$localStore.origin = origin;
  }

  moveToMainPage() {
    this.$router.push('/main');
  }

  moveToSignUpPage() {
    this.$router.push('/signup');
  }

  moveToSignUpAdminPage() {
    this.$router.push('/signup/admin');
  }

  testInit() {
    this.updateState(LoginPageState.Connecting);

    this.$api2.testInit()
        .then(_ => {
          this.updateState(LoginPageState.ReadyForWait);
          setTimeout(() => {
            this.updateState(LoginPageState.Ready);
          }, this.waitMoment);
        })
        .catch(error => {
          if (error.response) {
            if (error.response.status && error.response.status == 520) {
              this.moveToSignUpAdminPage();
            } else {
              this.updateState(LoginPageState.Unreachable);
            }
          } else {
            this.updateState(LoginPageState.Unreachable);
          }
        });
  }

  updateState(state: LoginPageState): void {
    const oldVal = LoginPageState[this.currentState];
    const newVal = LoginPageState[state];
    this.currentState = state;
    console.debug(`Change login page state: ${oldVal} -> ${newVal}`);
  }

  showErrorMessage(message: string) {
    this.errorMessage = message;
  }

  hideErrorMessage() {
    this.errorMessage = '';
  }

  validateForms(): boolean {
    const validate = V_TEXT_FIELD_VALIDATE_METHOD_NAME;
    const fields = [this.$refs.usernameField, this.$refs.passwordField];
    let result = true;
    for (const key in fields) {
      const field = fields[key];
      if (field.hasOwnProperty(validate)) {
        // You need to repeat the validation function for every field.
        if (!field[validate](true)) {
          result = false;
        }
      }
    }
    return result;
  }

  // Events

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
    if (!this.validateForms()) {
      return;
    }

    const username = this.currentUsername;
    const password = this.currentPassword;
    console.debug(`User ${username} is trying to login ...`);
    this.showLoading = true;

    this.$api2.login(username, password)
        .then(response => {
          console.debug(`Login for user ${username} was successful !!`);

          this.showLoading = false;
          this.hideErrorMessage();

          const access = response.access || '';
          const refresh = response.refresh || '';
          const user = response.user || {} as User;
          this.saveUserToLocal(access, refresh, user);
          this.saveUserToSession(access, refresh, user);

          this.moveToMainPage();
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
          const msg = this.$t('msg.invalid_fields').toString();
          this.showErrorMessage(msg);
        });
  }

  onClickSignup() {
    this.moveToSignUpPage();
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
