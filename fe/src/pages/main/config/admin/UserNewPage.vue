<i18n lang="yaml">
en:
  title: "Add user"
  subtitle: "Register a new user"
  header:
    account: "Account"

ko:
  title: "사용자 추가"
  subtitle: "새로운 사용자를 등록합니다."
  header:
    account: "Account"
</i18n>

<template>
  <v-container>
    <app-bar-title
        flat
        :title="$t('title')"
        :subtitle="$t('subtitle')"
    ></app-bar-title>

    <v-list flat subheader three-line>
      <v-subheader>{{ $t('header.account') }}</v-subheader>

<!--      <v-list-item>-->
<!--        <v-text-field-->
<!--            type="text"-->
<!--            autocomplete="off"-->
<!--            ref="usernameField"-->
<!--            v-model="currentUsername"-->
<!--            :rules="[rules.username.required]"-->
<!--            :label="usernameFieldLabel"-->
<!--        ></v-text-field>-->
<!--      </v-list-item>-->

<!--      <v-list-item>-->
<!--        <v-text-field-->
<!--            type="password"-->
<!--            autocomplete="off"-->
<!--            ref="passwordField"-->
<!--            v-model="currentPassword"-->
<!--            :rules="[rules.password.required]"-->
<!--            :label="passwordFieldLabel"-->
<!--        ></v-text-field>-->
<!--      </v-list-item>-->

      <v-divider></v-divider>

    </v-list>

    <!--Account-->
    <!--Name-->
    <!--* required-->
    <!--Username-->
    <!--* required-->
    <!--Email-->
    <!--* required-->
    <!--Password-->


  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

@Component
export default class UserNewPage extends Vue {
}
</script>
