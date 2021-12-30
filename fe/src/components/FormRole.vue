<i18n lang="yaml">
en:
  labels:
    slug: "Slug"
    name: "Name"
    description: "Description"
    permissions: "Permissions"
    hidden: "Hidden"
    lock: "Lock"
  hints:
    slug: "Permission slug to be used in the URL."
    name: "The name of the permission as it is displayed on the screen."
    description: "A specific description of the permission."
    hidden: "When enabled, it is not visible to the user."
    lock: "When enabled, it cannot be edited or removed."
  msgs:
    empty: "No permissions selected."
  add: "Add"
  cancel: "Cancel"
  submit: "Submit"

ko:
  labels:
    slug: "슬러그"
    name: "이름"
    description: "설명"
    permissions: "권한"
    hidden: "숨김"
    lock: "잠금"
  hints:
    slug: "URL 경로에 사용될 권한 슬러그."
    name: "화면에 출력되는 권한명."
    description: "권한의 구체적인 설명."
    hidden: "활성화되면 사용자에게 표시되지 않습니다."
    lock: "활성화되면 편집하거나 제거할 수 없습니다."
  msgs:
    empty: "선택된 권한이 없습니다."
  add: "추가"
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <p :class="subtitleClass">{{ $t('labels.slug') }}</p>
    <v-text-field
        dense
        :value="value.slug"
        @input="inputSlug"
        :rules="slugRules"
        :disabled="disableSlug || disableAllIgnoreLock"
        :filled="disableSlug"
        :persistent-hint="!disableSlug"
        :hide-details="disableSlug"
        :hint="$t('hints.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.name') }}</p>
    <v-text-field
        dense
        :disabled="disableAllIgnoreLock"
        :value="value.name"
        @input="inputName"
        persistent-hint
        :hint="$t('hints.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.description') }}</p>
    <v-textarea
        dense
        auto-grow
        persistent-hint
        :disabled="disableAllIgnoreLock"
        :value="value.description"
        @input="inputDescription"
        :hint="$t('hints.description')"
    ></v-textarea>

    <p :class="subtitleClass">{{ $t('labels.permissions') }}</p>
    <v-sheet outlined>
      <div class="ma-1">
        <span
            v-if="!value.permissions || value.permissions.length === 0"
            :class="captionClass"
        >
          {{ $t('msgs.empty') }}
        </span>
        <div class="my-2 mx-4" v-else>
          <div
              class="d-flex flex-row align-center"
              v-for="perm in value.permissions"
              :key="perm"
          >
            <span class="text-caption text--secondary">
              {{ permissionName(perm) }}
            </span>
            <v-spacer></v-spacer>
            <v-btn
                icon
                small
                :disabled="disableAllIgnoreLock"
                @click="onClickPermissionRemove(perm)"
            >
              <v-icon>mdi-minus</v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <v-divider v-if="!disableAllIgnoreLock"></v-divider>
      <div
          class="my-2 mx-4 d-flex flex-row align-center"
          v-if="!disableAllIgnoreLock"
      >
        <v-select
            dense
            rounded
            outlined
            hide-details
            :items="permissionItems"
            v-model="selectPermission"
        ></v-select>
        <v-btn
            class="ml-4"
            elevation="2"
            small
            icon
            @click="onClickPermissionAdd"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </div>
    </v-sheet>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('labels.hidden') }}</p>
        <p class="text-caption text--secondary">{{ $t('hints.hidden') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
            inset
            :disabled="disableAllIgnoreLock"
            :value="value.hidden"
            @change="onChangeHidden"
        ></v-switch>
      </div>
    </v-row>

    <v-row class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('labels.lock') }}</p>
        <p class="text-caption text--secondary">{{ $t('hints.lock') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
            inset
            :value="value.lock"
            @change="onChangeLock"
        ></v-switch>
      </div>
    </v-row>

    <v-row v-if="!hideButtons" class="mt-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          v-if="!hideCancelButton"
          class="mr-4"
          color="second"
          @click="onClickCancel"
      >
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
          v-if="!hideSubmitButton"
          color="primary"
          :loading="loading"
          :disabled="disableSubmit"
          @click="onClickSubmit"
      >
        {{ $t('submit') }}
      </v-btn>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Ref, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {VSelectItem} from '@/hints/vuetify';
import {PERMISSION_SLUG_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';
import type {RoleA} from '@/packet/role';
import {getPermissionName} from '@/translations';
import {EmptyException} from '@/exceptions';

@Component
export default class FormRole extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;
  readonly slugRules = PERMISSION_SLUG_RULES;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableSlug!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly disableAllIgnoreLock!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Array, default: () => []})
  readonly permissions!: Array<string>;

  @Prop({type: Object, default: () => new Object()})
  readonly value!: RoleA;

  @Ref()
  readonly form!: VForm;

  valid = false;
  permissionItems = [] as Array<VSelectItem>;
  selectPermission = '';

  created() {
    this.updatePermissionItems(this.permissions);
  }

  @Watch('permissions')
  watchPermissions(newVal: Array<string>) {
    this.updatePermissionItems(newVal);
  }

  @Watch('value')
  watchValue() {
    this.updatePermissionItems(this.permissions);
  }

  updatePermissionItems(permissions: Array<string>) {
    this.permissionItems = permissions
        .map(x => {
          return {text: getPermissionName(x), value: x};
        }).filter(x => {
          if (!this.value.permissions) {
            return true;
          }
          return this.value.permissions.indexOf(x.value) === -1;
        });
    this.permissionItems.sort((x, y) => {
      return x.text.toString().localeCompare(y.text.toString());
    });
  }

  permissionName(perm: string) {
    return getPermissionName(perm);
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

  onChangeHidden(event: null | boolean) {
    this.value.hidden = !!event;
    this.input();
  }

  onChangeLock(event: null | boolean) {
    this.value.lock = !!event;
    this.input();
  }

  get disableSubmit() {
    return this.loading || !this.valid || this.disableSubmitButton;
  }

  formValidate() {
    this.form['validate']();
  }

  onClickPermissionRemove(perm: string) {
    if (!this.value.permissions) {
      throw new EmptyException('Empty permissions exception');
    }

    const index = this.value.permissions.indexOf(perm);
    this.value.permissions.splice(index, 1);
    if (this.value.permissions.length === 0) {
      this.value.permissions = undefined; // IMPORTANT: Reactive of vue
    }

    this.permissionItems.push({
      text: getPermissionName(perm),
      value: perm,
    });
    this.permissionItems.sort((x, y) => {
      return x.text.toString().localeCompare(y.text.toString());
    });

    this.selectPermission = '';
    this.input();
  }

  onClickPermissionAdd() {
    const index = this.permissionItems.findIndex(x => {
      return x.value == this.selectPermission;
    });
    this.permissionItems.splice(index, 1);

    if (this.value.permissions) {
      this.value.permissions.push(this.selectPermission);
    } else {
      this.value.permissions = [this.selectPermission];
    }

    this.selectPermission = '';
    this.input();
  }

  onClickCancel() {
    this.cancel();
  }

  onClickSubmit() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.submit();
  }

  @Emit()
  input() {
    return this.value;
  }

  @Emit()
  cancel() {
    // EMPTY
  }

  @Emit()
  submit() {
    return this.value;
  }
}
</script>
