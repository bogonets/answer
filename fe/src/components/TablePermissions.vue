<i18n lang="yaml">
en:
  header:
    name: "Name"
    read: "Read"
    write: "Write"
  label:
    layout: "Layout"
    storage: "Storage"
    manager: "Manager"
    graph: "Graph"
    member: "Member"
    setting: "Setting"
  tooltip:
    layout: "Permissions for page layout"
    storage: "Permissions for filesystem"
    manager: "Permissions for maintenance"
    graph: "Permissions for logic control"
    member: "Permissions for member management"
    setting: "Permissions for setting features"

ko:
  header:
    name: "이름"
    read: "읽기"
    write: "쓰기"
  label:
    layout: "레이아웃"
    storage: "저장소"
    manager: "관리자"
    graph: "그래프"
    member: "회원"
    setting: "설정"
  tooltip:
    layout: "페이지 배치를 위한 권한"
    storage: "파일 시스템 접근 권한"
    manager: "유지보수를 위한 권한"
    graph: "로직 제어를 위한 권한"
    member: "회원 관리를 위한 권한"
    setting: "기능 설정을 위한 권한"
</i18n>

<template>
  <v-simple-table dense>
    <template v-slot:default>
      <thead>
      <tr>
        <th class="text-start">
          {{ $t('header.name') }}
        </th>
        <th class="text-center checkbox-header">
          {{ $t('header.read') }}
        </th>
        <th class="text-center checkbox-header">
          {{ $t('header.write') }}
        </th>
      </tr>
      </thead>
      <tbody>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <tr v-bind="attrs" v-on="on">
            <td :class="tableDataClass">{{ $t('label.layout') }}</td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.r_layout"
                  @input="inputLayoutRead"
              ></v-simple-checkbox>
            </td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.w_layout"
                  @input="inputLayoutWrite"
              >
              </v-simple-checkbox>
            </td>
          </tr>
        </template>
        <span>
          {{ $t('tooltip.layout') }}
        </span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <tr v-bind="attrs" v-on="on">
            <td :class="tableDataClass">{{ $t('label.storage') }}</td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.r_storage"
                  @input="inputStorageRead"
              >
              </v-simple-checkbox>
            </td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.w_storage"
                  @input="inputStorageWrite"
              >
              </v-simple-checkbox>
            </td>
          </tr>
        </template>
        <span>
          {{ $t('tooltip.storage') }}
        </span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <tr v-bind="attrs" v-on="on">
            <td :class="tableDataClass">{{ $t('label.manager') }}</td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.r_manager"
                  @input="inputManagerRead"
              >
              </v-simple-checkbox>
            </td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.w_manager"
                  @input="inputManagerWrite"
              >
              </v-simple-checkbox>
            </td>
          </tr>
        </template>
        <span>
          {{ $t('tooltip.manager') }}
        </span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <tr v-bind="attrs" v-on="on">
            <td :class="tableDataClass">{{ $t('label.graph') }}</td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.r_graph"
                  @input="inputGraphRead"
              >
              </v-simple-checkbox>
            </td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.w_graph"
                  @input="inputGraphWrite"
              >
              </v-simple-checkbox>
            </td>
          </tr>
        </template>
        <span>
          {{ $t('tooltip.graph') }}
        </span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <tr v-bind="attrs" v-on="on">
            <td :class="tableDataClass">{{ $t('label.member') }}</td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.r_member"
                  @input="inputMemberRead"
              >
              </v-simple-checkbox>
            </td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.w_member"
                  @input="inputMemberWrite"
              >
              </v-simple-checkbox>
            </td>
          </tr>
        </template>
        <span>
          {{ $t('tooltip.member') }}
        </span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <tr v-bind="attrs" v-on="on">
            <td :class="tableDataClass">{{ $t('label.setting') }}</td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.r_setting"
                  @input="inputSettingRead"
              >
              </v-simple-checkbox>
            </td>
            <td>
              <v-simple-checkbox
                  :disabled="disabled"
                  :class="checkboxClass"
                  :value="value.w_setting"
                  @input="inputSettingWrite"
              >
              </v-simple-checkbox>
            </td>
          </tr>
        </template>
        <span>
          {{ $t('tooltip.setting') }}
        </span>
      </v-tooltip>

      </tbody>
    </template>
  </v-simple-table>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

const TABLE_DATA_CLASSES = [
  'text-start',
  'text--secondary',
  'text-overline',
];
export const TABLE_DATA_CLASS = TABLE_DATA_CLASSES.join(' ');

const CHECKBOX_CLASSES = [
  'd-flex',
  'align-center',
  'justify-center',
  'offsetting-margin-right',
];
export const CHECKBOX_CLASS = CHECKBOX_CLASSES.join(' ');

export class Perms {
  r_layout = false;
  w_layout = false;
  r_storage = false;
  w_storage = false;
  r_manager = false;
  w_manager = false;
  r_graph = false;
  w_graph = false;
  r_member = false;
  w_member = false;
  r_setting = false;
  w_setting = false;

  fromObject(obj?: any) {
    this.r_layout = obj?.r_layout || false;
    this.w_layout = obj?.w_layout || false;
    this.r_storage = obj?.r_storage || false;
    this.w_storage = obj?.w_storage || false;
    this.r_manager = obj?.r_manager || false;
    this.w_manager = obj?.w_manager || false;
    this.r_graph = obj?.r_graph || false;
    this.w_graph = obj?.w_graph || false;
    this.r_member = obj?.r_member || false;
    this.w_member = obj?.w_member || false;
    this.r_setting = obj?.r_setting || false;
    this.w_setting = obj?.w_setting || false;
  }
}

@Component
export default class TablePermissions extends VueBase {
  private readonly tableDataClass = TABLE_DATA_CLASS;
  private readonly checkboxClass = CHECKBOX_CLASS;

  @Prop({type: Boolean})
  readonly disabled!: boolean;

  @Prop({type: Object, default: new Perms()})
  readonly value!: Perms;

  inputLayoutRead(event: boolean) {
    this.value.r_layout = event;
    this.input();
  }

  inputLayoutWrite(event: boolean) {
    this.value.w_layout = event;
    this.input();
  }

  inputStorageRead(event: boolean) {
    this.value.r_storage = event;
    this.input();
  }

  inputStorageWrite(event: boolean) {
    this.value.w_storage = event;
    this.input();
  }

  inputManagerRead(event: boolean) {
    this.value.r_manager = event;
    this.input();
  }

  inputManagerWrite(event: boolean) {
    this.value.w_manager = event;
    this.input();
  }

  inputGraphRead(event: boolean) {
    this.value.r_graph = event;
    this.input();
  }

  inputGraphWrite(event: boolean) {
    this.value.w_graph = event;
    this.input();
  }

  inputMemberRead(event: boolean) {
    this.value.r_member = event;
    this.input();
  }

  inputMemberWrite(event: boolean) {
    this.value.w_member = event;
    this.input();
  }

  inputSettingRead(event: boolean) {
    this.value.r_setting = event;
    this.input();
  }

  inputSettingWrite(event: boolean) {
    this.value.w_setting = event;
    this.input();
  }

  @Emit()
  input() {
    return this.value;
  }
}
</script>

<style lang="scss" scoped>
.checkbox-header {
  width: 1px;
  max-width: 1px;
}

// A class for offsetting the `margin-right` property applied
// to the `.v-input--selection-controls__input` class.
.offsetting-margin-right {
  padding-left: 8px;
}
</style>
