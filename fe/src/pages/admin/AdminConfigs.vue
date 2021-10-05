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

    <v-subheader>{{ $t('headers.account') }}</v-subheader>
    <left-title
        small
        no-gutter
        no-wrap-xs
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.public_signup')"
        :subheader="$t('subtitles.public_signup')"
    >
      <div class="d-flex flex-row justify-end">
        <v-switch
            inset
            v-model="public_signup"
            @change="onChangePublicSignup"
        ></v-switch>
      </div>
    </left-title>

    <v-divider></v-divider>
    <v-subheader>{{ $t('headers.session') }}</v-subheader>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.access_token_duration')"
        :subheader="$t('subtitles.access_token_duration')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            v-model="access_token_duration"
            :items="durations"
            @change="onChangeAccessTokenDuration"
        ></v-combobox>
      </div>
    </left-title>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.refresh_token_duration')"
        :subheader="$t('subtitles.refresh_token_duration')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            v-model="refresh_token_duration"
            :items="durations"
            @change="onChangeRefreshTokenDuration"
        ></v-combobox>
      </div>
    </left-title>

    <v-divider></v-divider>
    <v-subheader>{{ $t('headers.http') }}</v-subheader>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.external_host')"
        :subheader="$t('subtitles.external_host')"
    >
      <div class="d-flex flex-row justify-end">
        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="external_host"
            @change="onChangeExternalHost"
        ></v-text-field>
      </div>
    </left-title>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.http_timeout')"
        :subheader="$t('subtitles.http_timeout')"
    >
      <div class="d-flex flex-row justify-end">
        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="http_timeout"
            @change="onChangeHttpTimeout"
        ></v-text-field>
      </div>
    </left-title>

    <v-divider></v-divider>
    <v-subheader>{{ $t('headers.task') }}</v-subheader>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.user')"
        :subheader="$t('subtitles.user')"
    >
      <div class="d-flex flex-row justify-end">
        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="user"
            @change="onChangeUser"
        ></v-text-field>
      </div>
    </left-title>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.group')"
        :subheader="$t('subtitles.group')"
    >
      <div class="d-flex flex-row justify-end">
        <v-text-field
            dense
            outlined
            hide-details
            type="text"
            autocomplete="off"
            v-model="group"
            @change="onChangeGroup"
        ></v-text-field>
      </div>
    </left-title>

    <v-divider></v-divider>
    <v-subheader>{{ $t('headers.logging') }}</v-subheader>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.log_level')"
        :subheader="$t('subtitles.log_level')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            v-model="log_level"
            :items="severities"
            @change="onChangeLogLevel"
        ></v-combobox>
      </div>
    </left-title>

    <left-title
        small
        no-gutter
        :left-ratio="8"
        :right-ratio="4"
        :header="$t('titles.verbose')"
        :subheader="$t('subtitles.verbose')"
    >
      <div class="d-flex flex-row justify-end">
        <v-combobox
            dense
            outlined
            hide-details
            v-model="verbose"
            :items="levels"
            @change="onChangeVerbose"
        ></v-combobox>
      </div>
    </left-title>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import {ConfigA, UpdateConfigValueQ} from '@/packet/config';

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

const CONFIG_KEY_PUBLIC_SIGNUP = 'public_signup';
const CONFIG_KEY_ACCESS_TOKEN_DURATION = 'access_token_duration';
const CONFIG_KEY_REFRESH_TOKEN_DURATION = 'refresh_token_duration';
const CONFIG_KEY_EXTERNAL_HOST = 'external_host';
const CONFIG_KEY_HTTP_TIMEOUT = 'http_timeout';
const CONFIG_KEY_USER = 'user';
const CONFIG_KEY_GROUP = 'group';
const CONFIG_KEY_LOG_LEVEL = 'log_level';
const CONFIG_KEY_VERBOSE = 'verbose';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
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

  private readonly durations = [
    '10 minutes',
    '30 minutes',
    '1 hour',
    '12 hours',
    '1 day',
    '7 days',
  ];

  private readonly severities = [
    'Critical',
    'Fatal',
    'Error',
    'Warning',
    'Warn',
    'Info',
    'Debug',
    'Notset',
    'Off',
  ];

  private readonly levels = [
    '0',
    '1',
    '2',
    '3',
  ];

  loading = false;
  public_signup = false;
  access_token_duration = '';
  refresh_token_duration = '';
  external_host = '';
  http_timeout = 0.0;
  user = '';
  group = '';
  log_level = '';
  verbose = 0;

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
    this.public_signup = findBoolean(items, CONFIG_KEY_PUBLIC_SIGNUP);
    this.access_token_duration = findString(items, CONFIG_KEY_ACCESS_TOKEN_DURATION);
    this.refresh_token_duration = findString(items, CONFIG_KEY_REFRESH_TOKEN_DURATION);
    this.external_host = findString(items, CONFIG_KEY_EXTERNAL_HOST);
    this.http_timeout = findFloat(items, CONFIG_KEY_HTTP_TIMEOUT);
    this.user = findString(items, CONFIG_KEY_USER);
    this.group = findString(items, CONFIG_KEY_GROUP);
    this.log_level = findString(items, CONFIG_KEY_LOG_LEVEL);
    this.verbose = findInteger(items, CONFIG_KEY_VERBOSE);
  }

  patchConfig(key: string, value: any) {
    const body = {
      value: value
    } as UpdateConfigValueQ;
    this.loading = true;
    this.$api2.patchAdminConfigsPkey(key, body)
        .then(() => {
          this.loading = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  onChangePublicSignup(value) {
    this.patchConfig(CONFIG_KEY_PUBLIC_SIGNUP, value);
  }

  onChangeAccessTokenDuration(value) {
    this.patchConfig(CONFIG_KEY_ACCESS_TOKEN_DURATION, value);
  }

  onChangeRefreshTokenDuration(value) {
    this.patchConfig(CONFIG_KEY_REFRESH_TOKEN_DURATION, value);
  }

  onChangeExternalHost(value) {
    this.patchConfig(CONFIG_KEY_EXTERNAL_HOST, value);
  }

  onChangeHttpTimeout(value) {
    this.patchConfig(CONFIG_KEY_HTTP_TIMEOUT, value);
  }

  onChangeUser(value) {
    this.patchConfig(CONFIG_KEY_USER, value);
  }

  onChangeGroup(value) {
    this.patchConfig(CONFIG_KEY_GROUP, value);
  }

  onChangeLogLevel(value) {
    this.patchConfig(CONFIG_KEY_LOG_LEVEL, value);
  }

  onChangeVerbose(value) {
    this.patchConfig(CONFIG_KEY_VERBOSE, value);
  }
}
</script>
