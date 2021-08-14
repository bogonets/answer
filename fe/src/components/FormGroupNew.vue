<i18n lang="yaml">
en:
  label:
    name: "Name (Required)"
    nickname: "Nickname"
    description: "Description (Optional)"
    features: "Features (Optional)"
  hint:
    name: "Group name to be used in the URL."
    nickname: "The nickname of the group as it is displayed on the screen."
    description: "A specific description of the group."
    features: "A list of features to apply to the group."
  no_matching: "No results matching \"{search}\". Press {key} to create a new one."
  cancel: "Cancel"
  submit: "Submit"

ko:
  label:
    name: "이름 (필수)"
    nickname: "별칭"
    description: "설명"
    features: "기능"
  hint:
    name: "URL에 사용될 그룹 이름."
    nickname: "화면에 출력되는 그룹의 별명."
    description: "그룹의 구체적인 설명."
    features: "그룹에 적용할 기능 목록 입니다."
  no_matching: "\"{search}\" 와 일치하는 결과가 없습니다. {key} 키를 눌러 추가할 수 있습니다."
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <subtitle bold>{{ $t('label.name') }}</subtitle>
    <v-text-field
        class="my-2"
        dense
        persistent-hint
        :disabled="disableName"
        :hint="$t('hint.name')"
        :rules="rules.name"
        :value="name"
    ></v-text-field>

    <subtitle bold>{{ $t('label.nickname') }}</subtitle>
    <v-text-field
        class="my-2"
        dense
        persistent-hint
        :hint="$t('hint.nickname')"
        :value="nickname"
    ></v-text-field>

    <subtitle bold>{{ $t('label.description') }}</subtitle>
    <v-textarea
        class="my-2"
        dense
        auto-grow
        persistent-hint
        :hint="$t('hint.description')"
        :value="description"
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
import {GROUP_NAME_RULES} from '@/rules';

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
    name: GROUP_NAME_RULES,
  };

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableName!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Ref()
  readonly form!: VForm;

  valid = false;
  name = '';
  nickname = '';
  description = '';
  features: Array<string> = [];

  searchFeature = '';
  featuresItems: Array<string> = [];

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
      name: this.name,
      nickname: this.nickname,
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
