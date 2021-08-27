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
            <form-user
                hide-cancel-button
                class="pa-4"
                hide-access
                hide-profile
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
import FormUser, {UserItem} from '@/components/FormUser.vue';
import {SignupQ} from '@/packet/user';

@Component({
  components: {
    FormUser,
  }
})
export default class Init extends VueBase {
  showSignupLoading = false;

  onClickOk(event: UserItem) {
    const body = {
      username: event.username,
      password: this.$api2.encryptPassword(event.password),
    } as SignupQ;

    this.showSignupLoading = true;
    this.$api2.postPublicSignupAdmin(body)
        .then(() => {
          this.showSignupLoading = false;
          this.moveToSignin();
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
