<i18n lang="yaml">
en:
  label:
    private: 'Private'
    internal: 'Internal'
    public: 'Public'
  hint:
    private: 'Access must be explicitly granted to each user.'
    internal: 'Any logged in user can access.'
    public: 'Access is allowed without authentication.'

ko:
  label:
    private: '비공개'
    internal: '내부'
    public: '공개'
  hint:
    private: '접근 권한은 각 사용자에게 명시적으로 부여되어야 합니다.'
    internal: '로그인한 모든 사용자가 접근할 수 있습니다.'
    public: '인증 없이 접근할 수 있습니다.'
</i18n>

<template>
  <v-radio-group dense persistent-hint :value="value" @change="input">
    <v-radio :value="levelPrivate">
      <template v-slot:label>
        <div class="d-flex flex-column">
          <div class="text-body-2 text--primary">
            {{ $t('label.private') }}
          </div>
          <div class="text-caption text--secondary">
            {{ $t('hint.private') }}
          </div>
        </div>
      </template>
    </v-radio>
    <v-radio :value="levelInternal">
      <template v-slot:label>
        <div class="d-flex flex-column">
          <div class="text-body-2 text--primary">
            {{ $t('label.internal') }}
          </div>
          <div class="text-caption text--secondary">
            {{ $t('hint.internal') }}
          </div>
        </div>
      </template>
    </v-radio>
    <v-radio v-if="!hidePublic" :value="levelPublic">
      <template v-slot:label>
        <div class="d-flex flex-column">
          <div class="text-body-2 text--primary">
            {{ $t('label.public') }}
          </div>
          <div class="text-caption text--secondary">
            {{ $t('hint.public') }}
          </div>
        </div>
      </template>
    </v-radio>
  </v-radio-group>
</template>

<script lang="ts">
import {Vue, Component, Prop, Emit} from 'vue-property-decorator';

export const LEVEL_PRIVATE = 0;
export const LEVEL_INTERNAL = 10;
export const LEVEL_PUBLIC = 20;

@Component
export default class RadioVisibility extends Vue {
  private readonly levelPrivate = LEVEL_PRIVATE;
  private readonly levelInternal = LEVEL_INTERNAL;
  private readonly levelPublic = LEVEL_PUBLIC;

  @Prop({type: Boolean, default: true})
  readonly hidePublic!: boolean;

  @Prop({type: Number, default: LEVEL_PRIVATE})
  readonly value!: number;

  @Emit()
  input(value: number) {
    return value;
  }
}
</script>
