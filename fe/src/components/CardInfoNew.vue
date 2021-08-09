<i18n lang="yaml">
en:
  title: "New info"
  subtitle: "You can add new environment variables."
  label:
    key: "Key"
    value: "Value"
  msg:
    required_field: "Required field"
  cancel: "Cancel"
  ok: "Ok"

ko:
  title: "설정 추가"
  subtitle: "새로운 환경 변수를 추가할 수 있습니다."
  label:
    key: "열쇠 (Key)"
    value: "값 (Value)"
  msg:
    required_field: "공백을 허용하지 않습니다."
  cancel: "취소"
  ok: "확인"
</i18n>

<template>
  <v-card>
    <v-card-title class="mb-1">{{ $t('title') }}</v-card-title>
    <v-card-subtitle>{{ $t('subtitle') }}</v-card-subtitle>

    <v-divider></v-divider>

    <v-container>
      <v-list flat>
        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              ref="keyField"
              v-model="infoKey"
              :rules="[rules.key.required]"
              :label="$t('label.key')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              v-model="infoValue"
              :label="$t('label.value')"
              @keydown.enter.stop="submit"
          ></v-text-field>
        </v-list-item>
      </v-list>
    </v-container>

    <v-divider></v-divider>

    <v-card-actions>
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
          @click="submit"
      >
        {{ $t('ok') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Emit } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

const V_TEXT_FIELD_VALIDATE = 'validate';

@Component
export default class CardInfoNew extends VueBase {

  private readonly rules = {
    key: {
      required: (text) => {
        return !!text || this.$t('msg.required_field');
      },
    },
  };

  infoKey = '';
  infoValue = '';

  mounted() {
    this.infoKey = '';
    this.infoValue = '';
  }

  validateForms(): boolean {
    const fields = [this.$refs.keyField];
    let result = true;
    for (const key in fields) {
      const field = fields[key];
      if (!field) {
        continue;
      }

      const validate = field[V_TEXT_FIELD_VALIDATE];
      if (validate === undefined) {
        continue;
      }

      // You need to repeat the validation function for every field.
      if (!validate(true)) {
        result = false;
      }
    }
    return result;
  }

  @Emit()
  cancel() {
    return {
      key: this.infoKey,
      value: this.infoValue,
    };
  }

  submit() {
    if (!this.validateForms()) {
      return;
    }
    this.ok();
  }

  @Emit()
  ok() {
    return {
      key: this.infoKey,
      value: this.infoValue,
    };
  }
}
</script>
