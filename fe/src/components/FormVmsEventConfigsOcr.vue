<i18n lang="yaml">
en:
  cancel: "Cancel"
  submit: "Submit"

ko:
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid" lazy-validation>

    <v-row v-if="!hideButtons" class="mt-4 mb-2" no-gutters>
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
import {Component, Emit, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

function createEmptyObject() {
  return {};
}

@Component
export default class FormVmsEventConfigsOcr extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmit!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: any;

  @Ref()
  readonly form!: VForm;

  valid = false;

  @Emit()
  input() {
    return this.value;
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
  cancel() {
  }

  @Emit()
  ok() {
  }
}
</script>
