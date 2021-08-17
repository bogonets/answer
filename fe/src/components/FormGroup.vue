<i18n lang="yaml">
en:
  label:
    slug: "Slug"
    name: "Name"
    description: "Description"
    features: "Features"
  hint:
    slug: "Group slug to be used in the URL."
    name: "The name of the group as it is displayed on the screen."
    description: "A specific description of the group."
    features: "A list of features to apply to the group."
  visibility:
    label: "Visibility level"
    hint: "Who will be able to see this group?"
    private:
      label: "Private"
      hint: "The group and its projects can only be viewed by members."
    internal:
      label: "Internal"
      hint: "The group and any internal projects can be viewed by any logged in user."
    public:
      label: "Public"
      hint: "The group and any public projects can be viewed without any authentication."
  no_matching: "No results matching \"{search}\". Press {key} to create a new one."
  reset: "Reset"
  cancel: "Cancel"
  submit: "Submit"

ko:
  label:
    slug: "슬러그"
    name: "이름"
    description: "설명"
    features: "기능"
  hint:
    slug: "URL에 사용될 그룹 슬러그."
    name: "화면에 출력되는 그룹명."
    description: "그룹의 구체적인 설명."
    features: "그룹에 적용할 기능 목록 입니다."
  visibility:
    label: "Visibility level"
    hint: "Who will be able to see this group?"
    private:
      label: "Private"
      hint: "The group and its projects can only be viewed by members."
    internal:
      label: "Internal"
      hint: "The group and any internal projects can be viewed by any logged in user."
    public:
      label: "Public"
      hint: "The group and any public projects can be viewed without any authentication."
  no_matching: "\"{search}\" 와 일치하는 결과가 없습니다. {key} 키를 눌러 추가할 수 있습니다."
  reset: "복구"
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <p :class="subtitleClass">{{ $t('label.slug') }}</p>
    <v-text-field
        dense
        persistent-hint
        v-model="current.slug"
        :disabled="disableSlug"
        :hint="$t('hint.slug')"
        :rules="rules.slug"
        :prefix="slugPrefix"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.name') }}</p>
    <v-text-field
        dense
        persistent-hint
        v-model="current.name"
        :hint="$t('hint.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.description') }}</p>
    <v-textarea
        dense
        auto-grow
        persistent-hint
        v-model="current.description"
        :hint="$t('hint.description')"
    ></v-textarea>

    <p :class="subtitleClass">{{ $t('label.features') }}</p>
    <v-combobox
        dense
        hide-selected
        multiple
        small-chips
        persistent-hint
        v-model="current.features"
        :items="featureItems"
        :hint="$t('hint.features')"
        :search-input.sync="searchFeature"
    >
      <template v-slot:no-data>
        <p>
          <i18n class="py-1 px-4 text-body-2" path="no_matching" tag="span">
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
import {Component, Prop, Watch, Ref, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {GroupA} from '@/packet/group';
import {GROUP_SLUG_RULES} from '@/rules';

const SUBTITLE_CLASSES = [
  'text-subtitle-2',
  'text--secondary',
  'font-weight-bold',
  'my-2',
];
const SUBTITLE_CLASS = SUBTITLE_CLASSES.join(' ');

@Component
export default class FormGroup extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS
  private readonly rules = {
    slug: GROUP_SLUG_RULES,
  };

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Array, default: () => { return []; }})
  readonly featureItems!: Array<string>;

  @Prop({type: Object, default: () => { return {}; }})
  readonly value!: GroupA;

  @Ref()
  readonly form!: VForm;

  valid = false;
  searchFeature = '';
  current = {
    slug: '',
    name: '',
    description: '',
    features: [],
  } as GroupA;

  created() {
    this.updateCurrent(this.value);
  }

  @Watch('value')
  onChangeValue(value: GroupA) {
    this.updateCurrent(value);
  }

  copyGroup(source: GroupA, destination: GroupA) {
    destination.slug = source?.slug || '';
    destination.name = source?.name || '';
    destination.description = source?.description || '';
    destination.features = source?.features || [];
  }

  updateCurrent(value: GroupA) {
    this.copyGroup(value, this.current);
  }

  get modified(): boolean {
    if (this.value.slug !== this.current.slug) {
      return true;
    }
    if (this.value.name !== this.current.name) {
      return true;
    }
    if (this.value.description !== this.current.description) {
      return true;
    }
    return this.value.features !== this.current.features;
  }

  get origin(): string {
    return window.location.origin;
  }

  get slugPrefix(): string {
    return this.origin + (this.origin[this.origin.length-1] === '/' ? '' : '/')
  }

  get disableSubmit(): boolean {
    return this.loading || !this.valid || !this.modified;
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
    return this.current;
  }

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit()
  ok() {
    return this.current;
  }
}
</script>
