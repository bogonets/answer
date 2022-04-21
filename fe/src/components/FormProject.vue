<i18n lang="yaml">
en:
  label:
    group: 'Group'
    slug: 'Slug'
    name: 'Name'
    description: 'Description'
    features: 'Features'
    visibility: 'Visibility level'
  hint:
    group: 'The slug of the group.'
    slug: 'Project slug to be used in the URL.'
    name: 'The name of the project as it is displayed on the screen.'
    description: 'A specific description of the project.'
    features: 'A list of features to apply to the project.'
    visibility: 'Who will be able to see this project?'
  visibility:
    private:
      label: 'Private'
      hint: 'Project access must be granted explicitly to each user.'
    internal:
      label: 'Internal'
      hint: 'The project can be accessed by any logged in user.'
    public:
      label: 'Public'
      hint: 'The project can be accessed without any authentication.'
  no_matching: 'No results matching "{search}". Press {key} to create a new one.'
  cancel: 'Cancel'
  submit: 'Submit'

ko:
  label:
    group: '그룹'
    slug: '슬러그'
    name: '이름'
    description: '설명'
    features: '기능'
    visibility: '가시성 수준'
  hint:
    group: '그룹의 슬러그.'
    slug: 'URL 경로에 사용될 프로젝트 슬러그.'
    name: '화면에 출력되는 프로젝트명.'
    description: '프로젝트의 구체적인 설명.'
    features: '프로젝트에 적용할 기능 목록 입니다.'
    visibility: '누가 이 그룹을 볼 수 있나요?'
  visibility:
    private:
      label: '비공개'
      hint: '프로젝트 접근 권한은 각 사용자에게 명시적으로 부여되어야 합니다.'
    internal:
      label: '내부'
      hint: '로그인한 모든 사용자가 프로젝트에 접근할 수 있습니다.'
    public:
      label: '공개'
      hint: '인증 없이 프로젝트에 접근할 수 있습니다.'
  no_matching: '"{search}" 와 일치하는 결과가 없습니다. {key} 키를 눌러 추가할 수 있습니다.'
  cancel: '취소'
  submit: '제출'
</i18n>

<template>
  <v-form ref="form" v-model="valid">
    <p :class="subtitleClass">{{ $t('label.group') }}</p>
    <v-select
      dense
      menu-props="auto"
      :items="groupItems"
      :value="value.group"
      @change="inputGroup"
      :rules="rules.groupSlug"
      :loading="loadingGroups"
      :disabled="disableGroup || loadingGroups"
      :filled="disableGroup"
      :persistent-hint="!disableGroup"
      :hide-details="disableGroup"
      :hint="$t('hint.group')"
    ></v-select>

    <p :class="subtitleClass">{{ $t('label.slug') }}</p>
    <v-text-field
      dense
      :value="value.slug"
      @input="inputSlug"
      :rules="rules.projectSlug"
      :disabled="disableSlug"
      :filled="disableSlug"
      :persistent-hint="!disableSlug"
      :hide-details="disableSlug"
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

    <p v-if="!hideFeatures" :class="subtitleClass">{{ $t('label.features') }}</p>
    <v-combobox
      v-if="!hideFeatures"
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

    <p v-if="!hideVisibility" :class="subtitleClass" class="mb-1">
      {{ $t('label.visibility') }}
    </p>
    <p v-if="!hideVisibility" class="text-caption text--secondary mb-1">
      {{ $t('hint.visibility') }}
    </p>
    <radio-visibility
      v-if="!hideVisibility"
      class="mt-0"
      :value="value.visibility"
      @input="inputVisibility"
    ></radio-visibility>

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
import {Component, Prop, Ref, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RadioVisibility from '@/components/RadioVisibility.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import {GROUP_SLUG_RULES, PROJECT_SLUG_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';

export class ProjectItem {
  group = '';
  slug = '';
  name = '';
  description = '';
  features = [] as Array<string>;
  visibility = 0;

  fromObject(obj?: any) {
    this.group = obj?.group || '';
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
  },
})
export default class FormProject extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;
  private readonly captionClass = CAPTION_CLASS;

  private readonly rules = {
    groupSlug: GROUP_SLUG_RULES,
    projectSlug: PROJECT_SLUG_RULES,
  };

  @Prop({type: Boolean})
  readonly loadingGroups!: boolean;

  @Prop({type: Boolean})
  readonly loadingSubmit!: boolean;

  @Prop({type: Boolean})
  readonly disableGroup!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly hideFeatures!: boolean;

  @Prop({type: Boolean})
  readonly hideVisibility!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Array})
  readonly groupItems!: Array<string>;

  @Prop({type: Array})
  readonly featureItems!: Array<string>;

  @Prop({type: String})
  readonly initGroup!: string;

  @Prop({type: Object, default: () => new ProjectItem()})
  readonly value!: ProjectItem;

  @Ref()
  readonly form!: VForm;

  valid = false;
  searchFeature = '';

  created() {
    if (!!this.initGroup) {
      this.value.group = this.initGroup;
    }
  }

  inputGroup(event: string) {
    this.value.group = event;
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

  inputFeatures(event: Array<string>) {
    this.value.features = event;
    this.input();
  }

  inputVisibility(event: number) {
    this.value.visibility = event;
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
