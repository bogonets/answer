<i18n lang="yaml">
en:
  title: "API Settings",
  subtitle: "You can change the API origin address.",
  origin_label: "API origin address",
  cancel: "Cancel"
  ok: "Ok"

ko:
  title: "API 설정",
  subtitle: "서버 주소를 변경할 수 있습니다.",
  origin_label: "API 서버 주소",
  cancel: "취소"
  ok: "확인"
</i18n>

<template>
  <v-card>
    <v-card-title>
      <span>{{ $t('title') }}</span>
    </v-card-title>

    <v-card-subtitle class="mt-1">
      <span>{{ $t('subtitle') }}</span>
    </v-card-subtitle>

    <v-card-text>
      <v-text-field
          required
          v-model="currentOrigin"
          :label="$t('origin_label')"
          @keypress.enter.stop="onOk"
      ></v-text-field>
    </v-card-text>

    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="onCancel">
        {{ $t('cancel') }}
      </v-btn>
      <v-btn color="primary" text @click="onOk">
        {{ $t('ok') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

const EVENT_CANCEL = 'cancel';
const EVENT_OK = 'ok';

@Component
export default class CardConfigApiOrigin extends Vue {

  private currentOrigin = '';

  @Prop({type: String, default: ''})
  readonly initOrigin!: string;

  @Prop({type: Boolean, default: false})
  readonly initApi!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initLocalStore!: boolean;

  // Lifecycle

  mounted() {
    this.currentOrigin = this.getInitOrigin();
  }

  getInitOrigin(): string {
    if (this.initOrigin) {
      return this.initOrigin;
    } else if (this.initApi) {
      return this.$api2.origin;
    } else if (this.initLocalStore) {
      return this.$localStore.origin;
    }
    return document.location.origin;
  }

  // Events

  onCancel() {
    this.currentOrigin = this.getInitOrigin();
    this.$emit(EVENT_CANCEL, this.currentOrigin);
  }

  onOk() {
    this.$emit(EVENT_OK, this.currentOrigin);
  }
}
</script>
