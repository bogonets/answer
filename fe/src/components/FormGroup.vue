<i18n lang="yaml">
en:
  label:
    slug: "Slug"
    name: "Name"
    description: "Description"
    features: "Features"
    visibility: "Visibility level"
  hint:
    slug: "Group slug to be used in the URL."
    name: "The name of the group as it is displayed on the screen."
    description: "A specific description of the group."
    features: "A list of features to apply to the group."
    visibility: "Who will be able to see this group?"
  no_matching: "No results matching \"{search}\". Press {key} to create a new one."
  cancel: "Cancel"
  submit: "Submit"

ko:
  label:
    slug: "슬러그"
    name: "이름"
    description: "설명"
    features: "기능"
    visibility: "가시성 수준"
  hint:
    slug: "URL 경로에 사용될 그룹 슬러그."
    name: "화면에 출력되는 그룹명."
    description: "그룹의 구체적인 설명."
    features: "그룹에 적용할 기능 목록 입니다."
    visibility: "누가 이 그룹을 볼 수 있나요?"
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
        :rules="rules.slug"
        :disabled="disableSlug"
        :filled="disableSlug"
        :persistent-hint="!disableSlug"
        :hide-details="disableSlug"
        :prefix="slugPrefix"
        :hint="$t('hint.slug')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.name') }}</p>
    <v-text-field
        dense
        persistent-hint
        :value="value.name"
        @input="inputName"
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

    <p :class="subtitleClass" class="mb-1">{{ $t('label.visibility') }}</p>
    <p class="text-caption text--secondary mb-1">{{ $t('hint.visibility') }}</p>
    <radio-visibility
        class="mt-0"
        :value="value.visibility"
        @input="inputVisibility"
    ></radio-visibility>

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
import RadioVisibility from '@/components/RadioVisibility.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import {GROUP_SLUG_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';

export class GroupItem {
  slug = '';
  name = '';
  description = '';
  features = [] as Array<string>;
  visibility = 0;

  fromObject(obj?: any) {
    this.slug = obj?.slug || '';
    this.name = obj?.name || '';
    this.description = obj?.description || '';
    this.features = obj?.features || [];
    this.visibility = obj?.visibility || 0;
  }
}

@Component({
  components: {
    RadioVisibility,
  }
})
export default class FormGroup extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;
  private readonly captionClass = CAPTION_CLASS;

  private readonly rules = {
    slug: GROUP_SLUG_RULES,
  };

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly hideOriginPrefix!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Array})
  readonly featureItems!: Array<string>;

  @Prop({type: Object, default: () => new GroupItem()})
  readonly value!: GroupItem;

  @Ref()
  readonly form!: VForm;

  valid = false;
  searchFeature = '';

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

  inputVisibility(event: number) {
    this.value.visibility = event;
    this.input();
  }

  get slugPrefix(): undefined | string {
    if (this.hideOriginPrefix) {
      return undefined;
    }
    const origin = window.location.origin;
    return origin + (origin[origin.length-1] === '/' ? '' : '/')
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
