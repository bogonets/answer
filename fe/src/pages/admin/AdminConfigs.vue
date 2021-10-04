<i18n lang="yaml">
en:
  headers:
    account: "Account"
    session: "Session"
    http: "HTTP"
    task: "Task"
    logging: "Logging"
  titles:
    public_signup: "Public sign-up enabled"
    access_token_duration: "Access Token duration"
    refresh_token_duration: "Refresh Token duration"
    external_host: "External Host"
    http_timeout: "HTTP Timeout"
    user: "User"
    group: "Group"
    log_level: "Log Level"
    verbose: "Verbose Level"
  subtitles:
    public_signup: >
      When enabled, any user visiting this site will be able to create an account.
    access_token_duration: "Expiration period for the access token."
    refresh_token_duration: "Renewal period for expired access tokens."
    external_host: "The external address of the site."
    http_timeout: "HTTP request/response timeout (seconds)"
    user: "Username to use when creating tasks"
    group: "Group name to use when creating the task"
    log_level: "The importance of log messages to be output."
    verbose: "Prints more specific logs."

ko:
  headers:
    account: "계정"
    session: "세션"
    http: "HTTP"
    task: "테스크"
    logging: "로그"
  titles:
    public_signup: "공개 가입 활성화"
    access_token_duration: "액세스(Access) 토큰 기간"
    refresh_token_duration: "갱신(Refresh) 토큰 기간"
    external_host: "외부 호스트"
    http_timeout: "HTTP 시간 초과"
    user: "사용자"
    group: "그룹"
    log_level: "로그 레벨"
    verbose: "상세한 (Verbose) 정도"
  subtitles:
    public_signup: >
      활성화하면 이 사이트를 방문하는 모든 사용자가 계정을 만들 수 있습니다.
    access_token_duration: "액세스 토큰의 만료 기간."
    refresh_token_duration: "만료된 액세스 토큰의 갱신 기간."
    external_host: "사이트의 외부 호스트 주소."
    http_timeout: "HTTP 요청/응답 시간 초과 (초)"
    user: "태스크 생성시 사용할 사용자 이름"
    group: "태스크 생성시 사용할 그룹 이름"
    log_level: "출력할 로그 메시지의 중요도."
    verbose: "더욱 구체적인 로그를 출력합니다."
</i18n>

<template>
  <v-container>

    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-list flat subheader three-line>
      <v-subheader>{{ $t('headers.account') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.public_signup') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.public_signup') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-switch inset v-model="public_signup"></v-switch>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>{{ $t('headers.session') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.access_token_duration') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.access_token_duration') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="access_token_duration"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.refresh_token_duration') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.refresh_token_duration') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="refresh_token_duration"
        ></v-text-field>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>{{ $t('headers.http') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.external_host') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.external_host') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="external_host"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.http_timeout') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.http_timeout') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="http_timeout"
        ></v-text-field>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>{{ $t('headers.task') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.user') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.user') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="user"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.group') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.group') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="group"
        ></v-text-field>
      </v-list-item>

      <v-divider></v-divider>
      <v-subheader>{{ $t('headers.logging') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.log_level') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.log_level') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="log_level"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('titles.verbose') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('subtitles.verbose') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="verbose"
        ></v-text-field>
      </v-list-item>

    </v-list>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import {ConfigA} from "@/packet/config";

export function findBoolean(items: Array<ConfigA>, key: string, defaultValue = false) {
  const config = items.find(x => x.key === key);
  if (config) {
    return config.value === 'True';
  } else {
    return defaultValue;
  }
}

export function findInteger(items: Array<ConfigA>, key: string, defaultValue = 0) {
  const config = items.find(x => x.key === key);
  if (config) {
    return Number.parseInt(config.value);
  } else {
    return defaultValue;
  }
}

export function findFloat(items: Array<ConfigA>, key: string, defaultValue = 0.0) {
  const config = items.find(x => x.key === key);
  if (config) {
    return Number.parseFloat(config.value);
  } else {
    return defaultValue;
  }
}

export function findString(items: Array<ConfigA>, key: string, defaultValue = '') {
  const config = items.find(x => x.key === key);
  if (config) {
    return config.value;
  } else {
    return defaultValue;
  }
}

@Component({
  components: {
    ToolbarBreadcrumbs
  }
})
export default class AdminConfigs extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Configs',
      disabled: true,
    },
  ];

  loading = false;

  user = '';
  group = '';
  log_level = '';
  verbose = 0;
  external_host = '';
  http_timeout = 0.0;
  public_signup = false;
  access_token_duration = '';
  refresh_token_duration = '';

  mounted() {
    this.updateConfigs();
  }

  updateConfigs() {
    this.loading = true;
    this.$api2.getAdminConfigs()
        .then(items => {
          this.updateFields(items);
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  updateFields(items: Array<ConfigA>) {
    this.user = findString(items, 'user');
    this.group = findString(items, 'group');
    this.log_level = findString(items, 'log_level');
    this.verbose = findInteger(items, 'verbose');
    this.external_host = findString(items, 'external_host');
    this.http_timeout = findFloat(items, 'http_timeout');
    this.public_signup = findBoolean(items, 'public_signup');
    this.access_token_duration = findString(items, 'access_token_duration');
    this.refresh_token_duration = findString(items, 'refresh_token_duration');
  }
}
</script>
