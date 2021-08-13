<i18n lang="yaml">
en:
  title: "Admin Sign Up"
  subtitle: "You must register the first administrator."

ko:
  title: "관리자 등록"
  subtitle: "첫 번째 관리자를 등록해야합니다."
</i18n>

<template>
  <v-main>
    <v-container fluid class="fill-height">
      <v-row align="center" justify="center">
        <v-col class="max-content-width">
          <v-card elevation="8">
            <v-card-title>{{ $t('title') }}</v-card-title>
            <v-card-subtitle>{{ $t('subtitle') }}</v-card-subtitle>
            <form-user-new
                hide-access
                hide-profile
                dense-footer
                :loading="showSignupLoading"
                @cancel="onClickCancel"
                @ok="onClickOk"
            ></form-user-new>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import FormUserNew from '@/components/FormUserNew.vue';
import {Signup} from '@/apis/api-v2';

@Component({
  components: {
    FormUserNew,
  }
})
export default class MainAdminUsersNew extends VueBase {
  showSignupLoading = false;

  onClickCancel() {
    this.moveToBack();
  }

  onClickOk(user) {
    const data = {
      username: user.username,
      password: user.password,
    } as Signup;

    this.showSignupLoading = true;
    this.$api2.signupAdmin(data)
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
