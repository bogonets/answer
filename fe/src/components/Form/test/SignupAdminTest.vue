<template>
  <v-card>
    <v-card-title style="font-size: 20px">
      <strong>{{$t('admin') + ' ' + $t('sign_up')}}</strong>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <v-form>
        <v-text-field
          v-model="username"
          :label="$t('user_name')"
          :error="usernameError"
          :error-messages="usernameMsg"
          @input="inputUsername"
          @keypress.tab = "nextt(e)"
          type="text"
          outline
          counter
          persistent-hint
          ref="username"
          tabindex="1"
        ></v-text-field>
        <v-text-field
          v-model="password"
          :label="$t('password')"
          :error="passwordError"
          :error-messages="passwrodMsg"
          @input="inputPassword"
          @keypress.tab = "nextt(e)"
          outline
          :counter="passwordShow"
          persistent-hint
          :append-icon= "passwordShow ? 'visibility' : 'visibility_off'" 
          :type="passwordShow ? 'text' : 'password'"
          autocomplete="off"
          @click:append="passwordShow = !passwordShow"
          ref="password"
          tabindex="2"
        ></v-text-field>
        <v-text-field
          v-model="confirmPassword"
          :label="$t('password_confirm')"
          :error="confirmError"
          :error-messages="confirmMsg"
          @input="inputConfirm"
          @keypress.tab = "nextt(e)"
          outline
          :counter="checkPasswordShow"
          persistent-hint
          :append-icon="checkPasswordShow ? 'visibility' : 'visibility_off'"
          :type="checkPasswordShow ? 'text' : 'password'"
          autocomplete="off"
          @click:append="checkPasswordShow = !checkPasswordShow"
          @keypress.enter.stop="onSignup"
          ref="confirm"
          tabindex="3"
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text color="info" @click="onSignup" :loading="signupLoading" tabindex="4">{{$t('sign_up')}}</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "afSignupAdmin",
  props:{

  },
  components:{

  },

  data(){
    return {
      username: null,
      password: null,
      confirmPassword: null,
      passwordShow: false,
      checkPasswordShow: false,

      usernameError: false,
      usernameMsg: "",

      passwordError: false,
      passwrodMsg: "",

      confirmError: false,
      confirmMsg: "",

      signupLoading: false,
    }
  },
  computed:{

  },
  methods:{
    inputUsername: function () {
      this.usernameError = false;
      this.usernameMsg = "";
    },

    inputPassword: function () {
      this.passwordError = false;
      this.passwrodMsg = "";
    },

    inputConfirm: function () {
      this.confirmError = false;
      this.confirmMsg = "";
    },

    checkForm: function () {
      if (!this.username || this.username === "") {
        this.usernameError = true;
        this.usernameMsg = this.$t("join_error_message.empty_id");
        return { where: "username", result: false, msg: this.$t('join_error_message.empty_id') };
      }
      if (!this.password || this.password === "") {
        this.passwordError = true;
        this.passwrodMsg = this.$t("join_error_message.empty_password");
        return { where: "password", result: false, msg: this.$t('join_error_message.empty_password') };
      }
      if (!this.confirmPassword || this.confirmPassword === "") {
        this.confirmError = true;
        this.confirmMsg = this.$t("join_error_message.empty_password");
        return { where: "confirm", result: false, msg: this.$t('join_error_message.empty_password') };
      }
      if (this.password === this.confirmPassword) {
        return { where: "confirm", result: true, msg: this.$t('sign_up') + ' ' + this.$t('success') };
      } else {
        this.confirmError = true;
        this.confirmMsg = this.$t("join_error_message.not_match_password");
        return { where: "confirm", result: false, msg: this.$t('join_error_message.not_match_password') };
      }
    },

    makeSignupData: function () {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          var signupData = {
            id: this.username,
            password: this.$util.makeHash(this.password)
          }
          resolve(signupData);
        }, 1000)
      })
    },

    asyncSignup: async function () {
      await this.makeSignupData()
      .then(res1 => { 
        this.$api.checkAdmin()
        .then(res2 => {
          if (res2.data.status === "OK") {
            this.$warn(this.$options.name, "asyncSignup", "Existed admin.");
            alert(this.$options.name, "asyncSignup", "Existed admin.");
            this.$router.push("/");
            return;
          } else {
            this.$api.signupAdmin(res1)
            .then(res3 => {
              this.$debug(this.$options.name, "asyncSingup", "Signup Admin Success. Goto Login  page.");
              this.$router.push("/");
            })
            .catch(err3 => {
              this.$error(this.$options.name, "asyncSingup", "Signup Admin Failed. Detail:", err3);
            })
          }
        })
        .catch(err2 => {
          this.$warn(this.$options.name, "asyncSignup", "CheckAdmin Error. Detail:", err2);
        })
      })
      this.signupLoading = false;
    },

    signup: function () {
      return new Promise((resolve, reject) => {
        this.$api.signupAdmin(this.username, this.password)
        .then(res => {
          resolve(res);
        })
        .catch(err => {
          reject(err);
        })
      })
    },

    onSignup: function () {
      this.signupLoading = true;
      var checkData = this.checkForm();
      var where = checkData.where;
      var result = checkData.result;
      var msg = checkData.msg;
      if (result) {
        this.asyncSignup();
      } else {
        this.$refs[where].focus();
        this.signupLoading = false;
      }
    }
  },
  created(){

  },

  mounted(){
    this.$nextTick()
    .then(() => {
      this.$refs.username.focus()
    })
  }
}
</script>

<style scoped>

</style>
