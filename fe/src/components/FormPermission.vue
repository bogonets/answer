<i18n lang="yaml">
en:
  label:
    slug: "Slug"
    name: "Name"
    description: "Description"
    features: "Features"
    permissions: "Permissions"
    hidden: "Hidden"
    lock: "Lock"
  hint:
    slug: "Permission slug to be used in the URL."
    name: "The name of the permission as it is displayed on the screen."
    description: "A specific description of the permission."
    features: "A list of features to apply to the permission."
    hidden: "When enabled, it is not visible to the user."
    lock: "When enabled, it cannot be edited or removed."
  no_matching: "No results matching \"{search}\". Press {key} to create a new one."
  cancel: "Cancel"
  submit: "Submit"

ko:
  label:
    slug: "슬러그"
    name: "이름"
    description: "설명"
    features: "기능"
    permissions: "권한"
    hidden: "숨김"
    lock: "잠금"
  hint:
    slug: "URL 경로에 사용될 권한 슬러그."
    name: "화면에 출력되는 권한명."
    description: "프로젝트의 구체적인 설명."
    features: "프로젝트에 적용할 기능 목록 입니다."
    hidden: "활성화되면 사용자에게 표시되지 않습니다."
    lock: "활성화되면 편집하거나 제거할 수 없습니다."
  no_matching: "\"{search}\" 와 일치하는 결과가 없습니다. {key} 키를 눌러 추가할 수 있습니다."
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <p :class="subtitleClass">{{ $t('label.slug') }}</p>
    <v-text-field
        dense
        :value="value.slug"
        @input="inputSlug"
        :rules="slugRules"
        :disabled="disableSlug"
        :filled="disableSlug"
        :persistent-hint="!disableSlug"
        :hide-details="disableSlug"
        :hint="$t('hint.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.name') }}</p>
    <v-text-field
        dense
        :value="value.name"
        @input="inputName"
        persistent-hint
        :hint="$t('hint.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.description') }}</p>
    <v-textarea
        dense
        auto-grow
        persistent-hint
        :value="value.description"
        @input="inputDescription"
        :hint="$t('hint.description')"
    ></v-textarea>

    <p :class="subtitleClass">{{ $t('label.features') }}</p>
    <v-combobox
        dense
        hide-selected
        multiple
        small-chips
        persistent-hint
        :value="value.features"
        @input="inputFeatures"
        :items="featureItems"
        :hint="$t('hint.features')"
        :search-input.sync="searchFeature"
    >
      <template v-slot:no-data>
        <p>
          <i18n :class="captionClass" path="no_matching" tag="span">
            <template #search>
              <strong>{{ searchFeature }}</strong>
            </template>
            <template #key>
              <kbd>enter</kbd>
            </template>
          </i18n>
        </p>
      </template>
    </v-combobox>

    <p :class="subtitleClass">{{ $t('label.permissions') }}</p>
    <v-card flat outlined class="mb-4">
      <v-card-text class="pa-0">
        <table-permissions
            :value="value"
            @input="inputPerms"
        ></table-permissions>
      </v-card-text>
    </v-card>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('label.hidden') }}</p>
        <p class="text-caption text--secondary">{{ $t('hint.hidden') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
            inset
            :value="value.hidden"
            @change="onChangeHidden"
        ></v-switch>
      </div>
    </v-row>

    <v-row v-if="showLock" class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('label.lock') }}</p>
        <p class="text-caption text--secondary">{{ $t('hint.lock') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
            inset
            :value="value.lock"
            @change="onChangeLock"
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
          :loading="loading"
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
import TablePermissions, {Perms} from '@/components/TablePermissions.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import {PERMISSION_SLUG_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';

export class PermissionItem extends Perms {
  slug = '';
  name = '';
  description = '';
  features = [] as Array<string>;
  hidden = false;
  lock = false;

  fromObject(obj?: any) {
    this.slug = obj?.slug || '';
    this.name = obj?.name || '';
    this.description = obj?.description || '';
    this.features = obj?.features || [];
    this.hidden = obj?.hidden || false;
    this.lock = obj?.lock || false;
    super.fromObject(obj);
  }
}

@Component({
  components: {
    TablePermissions,
  }
})
export default class FormPermission extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;
  readonly slugRules = PERMISSION_SLUG_RULES;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly showLock!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

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

  @Prop({type: Array})
  readonly featureItems!: Array<string>;

  @Prop({type: Object, default: () => new PermissionItem()})
  readonly value!: PermissionItem;

  @Ref()
  readonly form!: VForm;

  valid = false;
  searchFeature = '';
  perms = new PermissionItem();

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

  inputFeatures(event: Array<string>) {
    this.value.features = event;
    this.input();
  }

  inputPerms(event: Perms) {
    (this.value as Perms).fromObject(event);
    this.input();
  }

  onChangeHidden(event: null | boolean) {
    this.value.hidden = !!event;
    this.input();
  }

  onChangeLock(event: null | boolean) {
    this.value.lock = !!event;
    this.input();
  }

  get disableSubmit(): boolean {
    return this.loading || !this.valid || this.disableSubmitButton;
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

<style lang="scss" scoped>
</style>
