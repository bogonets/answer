<i18n lang="yaml">
en:
  title: "Sign Up"

ko:
  title: "회원가입"
</i18n>

<template>
  <v-main>
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col class="max-content-width">
          <v-card elevation="8">
            <v-card-title>{{ $t('title') }}</v-card-title>
            <form-user
                class="pa-4"
                hide-access
                dense-footer
                :loading="showSignupLoading"
                @cancel="onClickCancel"
                @ok="onClickOk"
            ></form-user>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import FormUser from '@/components/FormUser.vue';
import {SignupQ} from '@/packet/user';

@Component({
  components: {
    FormUser,
  }
})
export default class MainAdminUsersNew extends VueBase {
  showSignupLoading = false;

  onClickCancel() {
    this.moveToBack();
  }

  onClickOk(user) {
    const body = {
      username: user.username,
      password: user.password,
      nickname: user.nickname,
      email: user.email,
      phone1: user.phone1,
      phone2: user.phone2,
    } as SignupQ;

    this.showSignupLoading = true;
    this.$api2.signup(body)
        .then(() => {
          this.showSignupLoading = false;
          this.moveToBack();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.showSignupLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>

<style lang="scss" scoped>
.max-content-width {
  max-width: 480px;
}
</style>
