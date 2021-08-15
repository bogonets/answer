<i18n lang="yaml">
en:
  label:
    slug: "Slug (Required)"
    name: "Name"
    description: "Description (Optional)"
    features: "Features (Optional)"
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
  cancel: "Cancel"
  submit: "Submit"

ko:
  label:
    slug: "슬러그 (필수)"
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
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <subtitle bold>{{ $t('label.slug') }}</subtitle>
    <v-row no-gutters>
      <v-text-field
          class="my-2"
          dense
          persistent-hint
          v-model="slug"
          :disabled="disableSlug"
          :hint="$t('hint.slug')"
          :rules="rules.slug"
          :prefix="slugPrefix"
      ></v-text-field>
    </v-row>

    <subtitle bold>{{ $t('label.name') }}</subtitle>
    <v-text-field
        class="my-2"
        dense
        persistent-hint
        v-model="name"
        :hint="$t('hint.name')"
    ></v-text-field>

    <subtitle bold>{{ $t('label.description') }}</subtitle>
    <v-textarea
        class="my-2"
        dense
        auto-grow
        persistent-hint
        v-model="description"
        :hint="$t('hint.description')"
    ></v-textarea>

    <subtitle bold>{{ $t('label.features') }}</subtitle>
    <v-combobox
        class="my-2"
        dense
        hide-selected
        multiple
        small-chips
        persistent-hint
        v-model="features"
        :items="featuresItems"
        :hint="$t('hint.features')"
        :search-input.sync="searchFeature"
    >
      <template v-slot:no-data>
        <subtitle>
          <i18n class="py-1 px-4 text-body-2" path="no_matching" tag="span">
            <template #search>
              <strong>{{ searchFeature }}</strong>
            </template>
            <template #key>
              <kbd>enter</kbd>
            </template>
          </i18n>
        </subtitle>
      </template>
    </v-combobox>

    <v-row no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          color="second"
          class="mr-4"
          @click="cancel"
      >
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
          color="primary"
          :loading="loading"
          :disabled="disableSubmit"
          @click="submit"
      >
        {{ $t('submit') }}
      </v-btn>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Ref, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import TextFieldThreeLine from '@/components/TextFieldThreeLine.vue';
import TextAreaThreeLine from '@/components/TextAreaThreeLine.vue';
import NameSlotHint from '@/components/NameSlotHint.vue';
import Subtitle from '@/components/Subtitle.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import {Group} from '@/apis/api-v2';
import {GROUP_SLUG_RULES} from '@/rules';

@Component({
  components: {
    Subtitle,
    NameSlotHint,
    LeftTitle,
    TextFieldThreeLine,
    TextAreaThreeLine,
  },
})
export default class FormGroupNew extends VueBase {
  private readonly rules = {
    slug: GROUP_SLUG_RULES,
  };

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Ref()
  readonly form!: VForm;

  valid = false;
  slug = '';
  name = '';
  description = '';
  features: Array<string> = [];

  searchFeature = '';
  featuresItems: Array<string> = [];

  get origin(): string {
    return window.location.origin;
  }

  get slugPrefix(): string {
    return this.origin + (this.origin[this.origin.length-1] === '/' ? '' : '/')
  }

  get disableSubmit(): boolean {
    return this.loading || !this.valid;
  }

  validate() {
    this.form['validate']();
  }

  reset() {
    this.form['reset']();
  }

  resetValidation() {
    this.form['resetValidation']();
  }

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit()
  ok() {
    return {
      slug: this.slug,
      name: this.name,
      description: this.description,
      features: this.features,
    } as Group;
  }

  submit() {
    if (!this.disableValidate) {
      this.validate();
      if (!this.valid) {
        return;
      }
    }

    this.ok();
  }
}
</script>
