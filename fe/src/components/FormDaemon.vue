<i18n lang="yaml">
en:
  labels:
    plugin: 'Plugin'
    slug: 'Slug'
    name: 'Name'
    address: 'Bind address'
    description: 'Description'
    enable: 'Enable'
  hints:
    plugin: 'The name of the plugin to use for the daemon.'
    slug: 'Daemon slug to be used in the URL.'
    name: 'The name of the daemon as it is displayed on the screen.'
    scheme: 'Scheme'
    host: 'Host'
    path: 'Path'
    abstract_path: 'Abstract path'
    address: 'Address'
    port: 'Port number'
    description: 'A specific description of the daemon.'
    enable: 'If enabled, it will run automatically on restart.'
  schemes:
    dns: 'DNS'
    unix: 'Unix'
    unix_abstract: 'Unix abstract'
    manually: 'Manually'
  cancel: 'Cancel'
  submit: 'Submit'

ko:
  labels:
    plugin: '플러그인'
    slug: '슬러그'
    name: '이름'
    address: '바인드 주소'
    description: '설명'
    enable: '활성화'
  hints:
    plugin: '데몬에 사용할 플러그인 이름.'
    slug: 'URL 경로에 사용될 데몬 슬러그.'
    name: '화면에 출력되는 데몬명.'
    scheme: '스키마'
    host: '호스트'
    path: '경로'
    abstract_path: '추상 경로'
    address: '주소'
    port: '포트 번호'
    description: '데몬의 구체적인 설명.'
    enable: '활성화하면 다시 시작할 때 자동으로 실행됩니다.'
  schemes:
    dns: 'DNS'
    unix: 'Unix'
    unix_abstract: 'Unix abstract'
    manually: '수동 입력'
  cancel: '취소'
  submit: '제출'
</i18n>

<template>
  <v-form ref="form" v-model="valid">
    <p :class="subtitleClass">{{ $t('labels.plugin') }}</p>
    <v-select
      dense
      menu-props="auto"
      :items="plugins"
      :value="value.plugin"
      @change="inputPlugin"
      :rules="rulesPlugin"
      :loading="loadingPlugin"
      :disabled="disablePlugin"
      :filled="disablePlugin"
      :persistent-hint="!disablePlugin"
      :hide-details="disablePlugin"
      :hint="$t('hints.plugin')"
    ></v-select>

    <p :class="subtitleClass">{{ $t('labels.slug') }}</p>
    <v-text-field
      dense
      :rules="rulesSlug"
      :value="value.slug"
      @input="inputSlug"
      :disabled="disableSlug"
      :filled="disableSlug"
      :persistent-hint="!disableSlug"
      :hide-details="disableSlug"
      :hint="$t('hints.slug')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.name') }}</p>
    <v-text-field
      dense
      persistent-hint
      :value="value.name"
      @input="inputName"
      :hint="$t('hints.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.address') }}</p>
    <v-container class="pa-0">
      <v-row no-gutters>
        <v-col cols="4">
          <v-select
            class="mr-2"
            :items="schemes"
            item-text="text"
            item-value="value"
            dense
            persistent-hint
            v-model="scheme"
            @change="onChangeScheme"
            :hint="$t('hints.scheme')"
          ></v-select>
        </v-col>

        <v-col v-if="isDnsScheme" cols="5">
          <v-combobox
            class="mr-2"
            dense
            persistent-hint
            clearable
            :value="dnsHost"
            @input="inputDnsHost"
            :hint="$t('hints.host')"
            :items="dnsHostItems"
          ></v-combobox>
        </v-col>
        <v-col v-if="isDnsScheme" cols="3">
          <v-text-field
            dense
            persistent-hint
            type="number"
            :loading="dnsPortLoading"
            :disabled="dnsPortLoading"
            :value="dnsPort"
            @input="inputDnsPort"
            :hint="$t('hints.port')"
            append-icon="mdi-refresh"
            @click:append="onClickRefreshPort"
          ></v-text-field>
        </v-col>

        <v-col v-if="isUnixScheme" cols="8">
          <v-text-field
            dense
            persistent-hint
            clearable
            :value="unixPath"
            @input="inputUnixPath"
            :hint="$t('hints.path')"
          ></v-text-field>
        </v-col>

        <v-col v-if="isUnixAbstractScheme" cols="8">
          <v-text-field
            dense
            persistent-hint
            clearable
            :value="unixAbstractPath"
            @input="inputUnixAbstractPath"
            :hint="$t('hints.abstract_path')"
          ></v-text-field>
        </v-col>

        <v-col v-if="isManuallyScheme" cols="8">
          <v-text-field
            dense
            persistent-hint
            clearable
            :value="manuallyAddress"
            @input="inputManuallyAddress"
            :hint="$t('hints.address')"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>

    <p :class="subtitleClass">{{ $t('labels.description') }}</p>
    <v-textarea
      dense
      auto-grow
      persistent-hint
      :value="value.description"
      @input="inputDescription"
      :hint="$t('hints.description')"
    ></v-textarea>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('labels.enable') }}</p>
        <p class="text-caption text--secondary">{{ $t('hints.enable') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch inset :value="value.enable" @change="changeEnable"></v-switch>
      </div>
    </v-row>

    <v-row v-if="!hideButtons" class="mt-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn v-if="!hideCancelButton" class="mr-4" color="second" @click="cancel">
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
        v-if="!hideSubmitButton"
        color="primary"
        :loading="loadingSubmit"
        :disabled="disableSubmit"
        @click="onSubmit"
      >
        {{ $t('submit') }}
      </v-btn>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Ref, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RadioVisibility from '@/components/RadioVisibility.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import requiredField from '@/rules/required';
import {DAEMON_SLUG_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';
import type {DaemonA} from '@/packet/daemon';
import {InaccessibleAreaException} from '@/exceptions';

@Component({
  components: {
    RadioVisibility,
  },
})
export default class FormProject extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  readonly rulesPlugin = [requiredField];
  readonly rulesSlug = DAEMON_SLUG_RULES;

  readonly schemeDns = 'dns:';
  readonly schemeUnix = 'unix:';
  readonly schemeUnixAbstract = 'unix-abstract:';
  readonly schemeManually = 'manually';

  readonly schemes = [
    {
      text: this.$t('schemes.dns'),
      value: this.schemeDns,
    },
    {
      text: this.$t('schemes.unix'),
      value: this.schemeUnix,
    },
    {
      text: this.$t('schemes.unix_abstract'),
      value: this.schemeUnixAbstract,
    },
    {
      text: this.$t('schemes.manually'),
      value: this.schemeManually,
    },
  ];

  readonly dnsHostItems = ['localhost', '127.0.0.1', '[::1]', '0.0.0.0', '[::]'];

  @Prop({type: Boolean})
  readonly loadingPlugin!: boolean;

  @Prop({type: Boolean})
  readonly disablePlugin!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

  @Prop({type: Boolean})
  readonly loadingSubmit!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Array, default: () => []})
  readonly plugins!: Array<string>;

  @Prop({type: Object, default: () => new Object()})
  readonly value!: DaemonA;

  @Ref()
  readonly form!: VForm;

  valid = false;

  touchName = false;
  scheme = this.schemeDns;
  dnsHost = '';
  dnsPort = 0;
  dnsPortLoading = false;
  unixPath = '';
  unixAbstractPath = '';
  manuallyAddress = '';

  @Watch('value', {deep: true})
  watchValue(newVal: DaemonA) {
    if (newVal.address) {
      // [WARNING]
      // Do not change the 'if-else' order.
      if (newVal.address.startsWith(this.schemeDns)) {
        this.scheme = this.schemeDns;
        const suffix = newVal.address.substr(this.schemeDns.length);
        const colonIndex = suffix.indexOf(':');
        if (colonIndex === -1) {
          this.dnsHost = suffix;
        } else {
          this.dnsHost = suffix.substr(0, colonIndex);
          this.dnsPort = Number.parseInt(suffix.substr(colonIndex + 1));
        }
      } else if (newVal.address.startsWith(this.schemeUnixAbstract)) {
        this.scheme = this.schemeUnixAbstract;
        this.unixAbstractPath = newVal.address.substr(this.schemeUnixAbstract.length);
      } else if (newVal.address.startsWith(this.schemeUnix)) {
        this.scheme = this.schemeUnix;
        this.unixPath = newVal.address.substr(this.schemeUnix.length);
      } else {
        this.scheme = this.schemeManually;
        this.manuallyAddress = newVal.address;
      }
    }
  }

  get isDnsScheme() {
    return this.scheme === this.schemeDns;
  }

  get isUnixScheme() {
    return this.scheme === this.schemeUnix;
  }

  get isUnixAbstractScheme() {
    return this.scheme === this.schemeUnixAbstract;
  }

  get isManuallyScheme() {
    return this.scheme === this.schemeManually;
  }

  inputPlugin(event: string) {
    this.value.plugin = event;
    this.input();
  }

  inputSlug(event: string) {
    this.value.slug = event;
    if (!this.touchName) {
      this.$set(this.value, 'name', event);
    }
    this.input();
  }

  inputName(event: string) {
    this.touchName = !!event;
    this.value.name = event;
    this.input();
  }

  get dnsAddress() {
    return this.schemeDns + this.dnsHost + ':' + this.dnsPort;
  }

  get unixAddress() {
    return this.schemeUnix + this.unixPath;
  }

  get unixAbstractAddress() {
    return this.schemeUnixAbstract + this.unixAbstractPath;
  }

  inputDnsHost(event: string) {
    this.dnsHost = event;
    this.value.address = this.dnsAddress;
    this.input();
  }

  inputDnsPort(event: string) {
    this.dnsPort = Number.parseInt(event);
    this.value.address = this.dnsAddress;
    this.input();
  }

  inputUnixPath(event: string) {
    this.unixPath = event;
    this.value.address = this.unixAddress;
    this.input();
  }

  inputUnixAbstractPath(event: string) {
    this.unixAbstractPath = event;
    this.value.address = this.unixAbstractAddress;
    this.input();
  }

  inputManuallyAddress(event: string) {
    this.manuallyAddress = event;
    this.value.address = event;
    this.input();
  }

  inputDescription(event: string) {
    this.value.description = event;
    this.input();
  }

  inputAddress(event: string) {
    this.value.address = event;
    this.input();
  }

  changeEnable(event: null | boolean) {
    this.value.enable = !!event;
    this.input();
  }

  get disableSubmit(): boolean {
    return this.loadingSubmit || !this.valid || this.disableSubmitButton;
  }

  onChangeScheme() {
    switch (this.scheme) {
      case this.schemeDns:
        this.value.address = this.dnsAddress;
        break;
      case this.schemeUnix:
        this.value.address = this.unixAddress;
        break;
      case this.schemeUnixAbstract:
        this.value.address = this.unixAbstractAddress;
        break;
      case this.schemeManually:
        this.value.address = this.manuallyAddress;
        break;
      default:
        throw new InaccessibleAreaException();
    }
    this.input();
  }

  onClickRefreshPort() {
    this.dnsPortLoading = true;
    this.$api2
      .getAdminPortNext()
      .then(portNumber => {
        this.dnsPort = portNumber;
        this.value.address = this.dnsAddress;
        this.input();
        this.dnsPortLoading = false;
      })
      .catch(error => {
        this.dnsPortLoading = false;
        this.toastRequestFailure(error);
      });
  }

  formValidate() {
    this.form['validate']();
  }

  onSubmit() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.ok();
  }

  @Emit()
  input() {
    return this.value;
  }

  @Emit()
  cancel() {
    return this.value;
  }

  @Emit()
  ok() {
    return this.value;
  }
}
</script>
