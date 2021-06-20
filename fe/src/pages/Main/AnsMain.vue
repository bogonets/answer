<template>
  <div id="app">
    <v-app>
      <adr-navigation ref="pageNavigation"></adr-navigation>
      <adr-components />
      <atb-title-bar
        @openConsole="consoleSheet = !consoleSheet"
      ></atb-title-bar>
      <v-main>
        <adlg-add-layout />
        <router-view />
      </v-main>

      <v-bottom-sheet v-model="consoleSheet" persistent>
        <v-sheet height="450px" style="border: 1px solid;">
          <a-console ref="terminal" @close="consoleSheet = false"></a-console>
        </v-sheet>
      </v-bottom-sheet>

      <v-dialog
        :dark="$vuetify.theme.dark"
        v-model="loginDialog"
        persistent
        fullscreen
        max-width="450"
      >
        <v-container fluid fill-height class="dialog-overlay">
          <v-layout align-center justify-center>
            <v-flex xs12 sm6 md4 lg4 xl4>
              <v-card @keypress.enter.stop="onLogin" class="reloginCard">
                <v-card-title primary-title>
                  <div>
                    <div class="headline">{{ $t("sign_in") }}</div>
                    <span class="red--text detailFont">{{
                      $t("expired_time")
                    }}</span>
                  </div>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-form>
                    <v-text-field
                      ref="username"
                      id="idinput"
                      v-model="username"
                      prepend-icon="person"
                      name="id"
                      :label="$t('user_name')"
                      type="text"
                    ></v-text-field>
                    <v-text-field
                      v-model="password"
                      ref="password"
                      id="password"
                      prepend-icon="lock"
                      name="password"
                      :label="$t('password')"
                      type="password"
                    ></v-text-field>
                    <v-alert
                      :value="error"
                      type="error"
                      color="red accent-2"
                      outline
                      class="alertStyle"
                      >{{ error_message }}</v-alert
                    >
                  </v-form>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-btn flat @click="onLogout" color="error">
                    {{ $t("logout") }}
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn flat @click="onLogin" :loading="loginSignal">{{
                    $t("sign_in")
                  }}</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-dialog>
    </v-app>
  </div>
</template>

<script>
import atbTitleBar from "@/components/Titlebar/atbTitleBar";
import adrNavigation from "@/components/Drawer/adrNavigation";
import adrComponents from "@/components/Drawer/adrComponents";
import adlgAddLayout from "@/components/Dialog/adlgAddLayout";
import { Observable } from "rxjs";
// 제일 부모의 메인 페이지. 프로젝트 리스트를 검사하여 하나면 그 프로젝트로 이동, 여러개면 리스트페이지로 이동.

/**
 * User Main Page. this page have projects and groups datas.
 * @author hadoo, 2019-06-13
 */
export default {
  name: "AnswerMainPage",
  components: {
    atbTitleBar,
    adrNavigation,
    adrComponents,
    adlgAddLayout,
  },
  data() {
    return {
      consoleSheet: false,
      timer: null,

      loginDialog: false,
      username: null,
      password: null,
      loginToken: null,
      error: false,
      error_message: null,

      loginSignal: false,
    };
  },
  methods: {
    onKeypress: function(key) {
      // console.log(key);
    },
    /**
     * Run Check Login Expired time.
     * @public
     */
    runCheckExp: function() {
      this.timer = setInterval(() => {
        var token = this.$store.getters["user/getAccessToken"];
        if (token) {
          var decode = this.$util.decodeToken(token);
          var expire = decode.exp * 1000;
          var now = Date.now();
          if (now >= expire) {
            // try refresh token. or Re login.
            this.loginDialog = true;
            this.username = this.$store.getters["user/getUserID"];
            this.closeCheckExp();
            if (this)
              this.$nextTick().then(() => {
                if (this.$store.getters["user/getUserID"]) {
                  if (this.username) {
                    this.$refs.password.focus();
                  } else {
                    this.$refs.username.focus();
                  }
                }
              });
          } else {
            /* EMPTY */
          }
        } else {
          this.$router.push("/"); // Go to login page.
        }
      }, 10000);
    },

    /**
     * Close Check Login Expired time.
     * @public
     */
    closeCheckExp: function() {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },

    /**
     * Open Relogin dialog.
     * @public
     */
    openReloginDialog: function() {
      this.loginDialog = true;
      if (this.$store.getters["user/getUserId"]) {
        this.username = this.$store.getters["user/getUserID"];
      }
    },

    /**
     * Close Relogin dialog.
     * @public
     */
    closeReloginDialog: function() {
      this.username = null;
      this.password = null;
      this.loginToken = null;
      this.error = false;
      this.error_message = null;
      this.loginDialog = false;
    },

    /**
     * Check Username and Password.
     * @public
     */
    checkLoginInfo: function() {
      if (!this.username) {
        this.error = true;
        this.error_message = this.$t("login_error_message.empty_id");
        return false;
      } else if (!this.password) {
        this.error = true;
        this.error_message = this.$t("login_error_message.empty_password");
        return false;
      } else {
        return true;
      }
    },

    /**
     * The method that occurs when a login fails.
     * @param {string} - Catch Error Response value.
     * @public
     */
    showErrorAlert: function(err_msg) {
      this.error_message = err_msg || this.$t("incorrect_password");
      this.error = true;
      if (this.password) {
        this.password = null;
      }
    },

    /**
     * Login.
     * @public
     */
    onLogin: function() {
      if (this.checkLoginInfo()) {
        var code = this.username + ":" + this.$util.makeHash(this.password);
        this.loginToken = btoa(code);
        if (this.loginToken) {
          if (this.error) {
            this.error = false;
            this.error_message = null;
          }
          this.loginSignal = true;
        }
      }
    },

    /**
     * Logout.
     * @public
     */
    onLogout: function() {
      this.$store.commit("user/logout");
      this.$router.push("/");
      this.$debug(this.$options.name, "onLogout", "Expired Logout.");
    },
  },
  computed: {},
  watch: {},
  created() {
    // 'bogonet' is Fix from v1.1.0.
    // this.$store.commit("project/setSelectProject", { name: "bogonet" })
  },
  mounted() {
    this.runCheckExp();
    this.$router.push(this.$page.projects);
    // 현재는 프로젝트가 하나라고 가정하여 바로 프로젝트 페이지로 이동시킨다. --> Projects 페이지 생성으로 Projects 페이지로 이동한다.
  },
  beforeDestroy() {
    this.closeCheckExp();
  },
  subscriptions() {
    const $loginSignal = this.$watchAsObservable("loginSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((loginSignal) => loginSignal == true)
      .debounceTime(1000); // 1초 타이머.
    return {
      result: Observable.combineLatest($loginSignal, (loginSignal) => ({
        loginSignal,
      })).flatMap(({ loginSignal }) =>
        this.$api
          .onLogin(this.loginToken)
          .do((res) => {
            this.$debug(
              this.$options.name,
              "subscriptions::onLogin",
              "response:",
              res
            );
            this.$store.commit("user/login", {
              accessToken: res.data.result.accessToken,
              refreshToken: res.data.result.refreshToken,
              id: res.data.result.user.id,
              email: null,
              phone: null,
            });
            this.closeReloginDialog();
            this.runCheckExp();
          })
          .catch((err) => {
            this.$error(this.$options.name, "subscriptions::onLogin", err);
            if (err.status !== 200) {
              this.showErrorAlert(null);
            } else {
              this.showErrorAlert(this.$t("server_is_not_opend"));
            }
            return Observable.of(null);
          })
          .do(() => {
            this.loginSignal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
.reloginCard {
  border: 2px solid;
  border-radius: 10px;
}
.alertStyle {
  border-radius: 10px;
  height: 22px;
  max-height: 45px;
}
.detailFont {
  opacity: 0.7;
}
.dialog-overlay {
  -ms-user-select: none;
  -moz-user-select: -moz-none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  user-select: none;
  background-color: rgb(30, 30, 30);
  opacity: 0.98;
}
</style>
