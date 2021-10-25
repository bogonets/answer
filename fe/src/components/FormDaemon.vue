<i18n lang="yaml">
en:
  labels:
    plugin: "Plugin"
    slug: "Slug"
    name: "Name"
    address: "Address"
    description: "Description"
    enable: "Enable"
  hints:
    plugin: "The name of the plugin to use for the daemon."
    slug: "Daemon slug to be used in the URL."
    name: "The name of the daemon as it is displayed on the screen."
    address: "gRPC address for communication."
    description: "A specific description of the daemon."
    enable: "If enabled, it will run automatically on restart."
  cancel: "Cancel"
  submit: "Submit"

ko:
  labels:
    plugin: "플러그인"
    slug: "슬러그"
    name: "이름"
    address: "주소"
    description: "설명"
    enable: "활성화"
  hints:
    plugin: "데몬에 사용할 플러그인 이름."
    slug: "URL 경로에 사용될 데몬 슬러그."
    name: "화면에 출력되는 데몬명."
    address: "통신을 위한 gRPC 주소."
    description: "데몬의 구체적인 설명."
    enable: "활성화하면 다시 시작할 때 자동으로 실행됩니다."
  cancel: "취소"
  submit: "제출"
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
        persistent-hint
        :rules="rulesSlug"
        :value="value.slug"
        @input="inputSlug"
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
    <v-text-field
        dense
        persistent-hint
        :value="value.address"
        @input="inputAddress"
        :hint="$t('hints.address')"
    ></v-text-field>

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
        <v-switch
            inset
            :value="value.enable"
            @change="changeEnable"
        ></v-switch>
      </div>
    </v-row>

    <v-row v-if="!hideButtons" class="mt-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          v-if="!hideCancelButton"
          class="mr-4"
          color="second"
          @click="cancel"
      >
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
import {Component, Prop, Ref, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RadioVisibility from '@/components/RadioVisibility.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import requiredField from '@/rules/required';
import {DAEMON_SLUG_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';
import type {DaemonA} from '@/packet/daemon';
import {createEmptyDaemonA} from '@/packet/daemon';

@Component({
  components: {
    RadioVisibility,
  }
})
export default class FormProject extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  readonly rulesPlugin = [requiredField];
  readonly rulesSlug = DAEMON_SLUG_RULES;

  @Prop({type: Boolean})
  readonly loadingPlugin!: boolean;

  @Prop({type: Boolean})
  readonly disablePlugin!: boolean;

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

  @Prop({type: Array, default: []})
  readonly plugins!: Array<string>;

  @Prop({type: Object, default: createEmptyDaemonA})
  readonly value!: DaemonA;

  @Ref()
  readonly form!: VForm;

  valid = false;

  inputPlugin(event: string) {
    this.value.plugin = event;
    this.input();
  }

  inputSlug(event: string) {
    this.value.slug = event;
    this.input();
  }

  inputName(event: string) {
    this.value.name = event;
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
