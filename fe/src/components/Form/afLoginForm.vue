<template>
  <v-card class="elevation-5" @keydown.enter="onLogin">
    <!-- <img src="@/assets/bogonet_logo.png" alt="avatar" width="100%"> -->
    <v-card-text>
      <v-form>
        <v-text-field
          color="orange"
          ref="id_input"
          id="idinput"
          v-model="d_id"
          prepend-icon="person"
          name="id"
          :label="$t('user_name')"
          type="text"
        ></v-text-field>
        <v-text-field
          color="orange"
          v-model="d_password"
          id="password"
          prepend-icon="lock"
          name="password"
          :label="$t('password')"
          type="password"
          autocomplete="off"
        ></v-text-field>
        <v-alert :value="d_error" type="error" color="red accent-2">{{
          d_error_message
        }}</v-alert>
      </v-form>
    </v-card-text>

    <v-card-actions>
      <a class="text-button" @click="onSignup">{{ $t("sign_up") }}</a>
      <v-spacer></v-spacer>
      <v-btn
          :loading="d_signal"
          :disabled="d_signal"
          @click="onLogin"
      >
        {{ $t("sign_in") }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { Observable } from "rxjs";
/**
 * Login Form Component.
 * @author hadoo 2019-01-15
 */
export default {
  name: "afLoginForm",
  data() {
    return {
      d_id: "",
      d_password: "",
      d_token: "",
      d_error_message: "",
      d_error: false, // error message 표시여부.

      // d_loading: false, // 버튼 Indicator 값.

      d_debug: false, // Debug Status.

      templateSignal: false
    };
  },
  methods: {
    /**
     * Change ID and SH256 password to base64.
     * @public
     */
    makeToken: function() {
      var code = this.d_id + ":" + this.$util.makeHash(this.d_password);
      this.d_token = btoa(code);
    },
    /**
     * Click event of Login button. - Communicate information with API.
     * @public
     */
    onLogin: function() {
      if (this.d_id == "") {
        this.d_error = true;
        this.d_error_message = this.$t("login_error_message.empty_id");
        return;
      } else if (this.d_password == "") {
        this.d_error = true;
        this.d_error_message = this.$t("login_error_message.empty_password");
        return;
      }
      // this.d_loading = !this.d_loading;
      this.makeToken();
      if (this.d_debug) {
        this.loginDebug();
      } else {
        this.$store.commit("signal/setLoginSignal", { bool: true });
      }
    },
    /**
     * Click Event of Signup button. (Move Sign-up page.)
     * @public
     */
    onSignup: function() {
      this.$router.push(this.$page.signup);
    },
    /**
     * The method that occurs on successful login.
     * @param {object} - information(token, id, email, phone) of User
     * @public
     */
    loginComplete: function(res) {
      this.$store.commit("user/login", {
        accessToken: res.accessToken,
        refreshToken: res.refreshToken,
        id: res.user.id,
        email: res.user.email,
        phone: res.user.phone
      });
        this.templateSignal = true;
      setTimeout(() => {
        this.$store.commit("signal/setLoginSignal", { bool: false });
        this.moveMainPage();
      }, 1000);
    },
    moveMainPage: function() {
      this.$router.push(this.$page.main); // 로그인 성공 시 메인페이지로 이동.
    },
    /**
     * The method that occurs when a login fails.
     * @param {errorResponse} - Catch Error Response value.
     * @public
     */
    loginFail: function(err_msg) {
      this.d_error_message =
        err_msg || this.$t("login_error_message.invalid_id_password");
      this.d_error = true;
      this.$store.commit("signal/setLoginSignal", { bool: false });
      // this.initialize();
    },
    /**
     * This initialize values.
     * @public
     */
    initialize: function() {
      // this.d_loading = false;
      // this.d_signal = false;
      this.$store.commit("signal/setLoginSignal", { bool: false });
      this.d_id = "";
      this.d_password = "";
    },
    /**
     * This is Debug Login.
     * @public
     */
    loginDebug: function() {
      this.$store.commit("user/login", {
        token:
          "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MTk0MDU4OTksImlhdCI6MTU2MTYyMTEzOSwiUGVybSI6IjAsMSwyIn0.UJA0oJX93lCYLi7bbZXwd2t8CREHCTWsVaDYKSsTg78",
        id: "bogo",
        email: "bogo@gmail.com",
        phone: "01012341234"
      });
      // this.d_loading = false;
      // this.d_signal = false;
      this.$store.commit("signal/setLoginSignal", { bool: false });
      this.$router.push(this.$page.main); // 로그인 성공 시 메인페이지로 이동.
    }
  },
  computed: {
    d_signal() {
      return this.$store.getters["signal/getLoginSignal"];
    },
    d_loading() {
      return this.d_signal;
    }
  },
  mounted() {
    this.$refs.id_input.focus();
  },
  subscriptions() {
    const $templateSignal = this.$watchAsObservable("templateSignal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(templateSignal => templateSignal == true);

    const $d_signal = this.$watchAsObservable("d_signal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(d_signal => d_signal == true) // if signal is true.
      .debounceTime(1000); // 3초 타이머.
    return {
      result: Observable.combineLatest($d_signal, d_signal => ({
        d_signal
      })).flatMap(({ d_signal }) =>
        this.$api
          .onLogin(this.d_token)
          .do(res => {
            this.$debug(
              this.$options.name,
              "subscriptions::onLogin",
              "response:",
              res
            );
            this.loginComplete(res["data"]["result"]);
          })
          .catch(err => {
            this.$error(this.$options.name, "subscriptions::onLogin", err);
            if (err.status !== 200) {
              this.loginFail();
            } else {
              this.loginFail(this.$t("server_is_not_opend"));
            }
            return Observable.of(null);
          })
      ),
      // .do(() => { this.d_loading = false; this.d_signal = false; })

      getLambdaTemplateResult: Observable.combineLatest(
        $templateSignal,
        templateSignal => ({
          templateSignal
        })
      ).flatMap(({ templateSignal }) =>
        this.$api
          .getLambdaTemplates(this.$store.getters["user/getAccessToken"])
          .do(res => {
            this.$templateStore.commit("setLambdaTemplates", res.result.obj);
          })
          .catch(err => {})
          .do(() => {
            this.templateSignal = false;
          })
      )
    };
  }
};
</script>

<style scoped></style>
