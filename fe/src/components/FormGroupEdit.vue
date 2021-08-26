<i18n lang="yaml">
en:
  header:
    basic: "Edit group"
    detail: "Detail"
  subheader:
    basic: "You can edit the group's basic properties."
    detail: "Detailed information about this group."
  label:
    created_at: "Created At"
    updated_at: "Updated At"
    delete: "Delete a group"
  hint:
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this group?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    basic: "그룹 편집"
    detail: "상세 정보"
  subheader:
    basic: "그룹의 기본 속성을 편집할 수 있습니다."
    detail: "이 그룹에 대한 자세한 정보입니다."
  label:
    created_at: "그룹 생성일"
    updated_at: "그룹 갱신일"
    delete: "그룹 제거"
  hint:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 그룹을 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <div>
    <left-title
        :header="$t('header.basic')"
        :subheader="$t('subheader.basic')"
    >
      <form-group
          disable-slug
          hide-cancel-button
          hide-origin-prefix
          :disable-submit-button="!modified"
          :value="current"
          @input="onUpdateCurrent"
          :loading="loadingSubmit"
          @ok="onClickOk"
      ></form-group>
    </left-title>

    <left-title
        :header="$t('header.detail')"
        :subheader="$t('subheader.detail')"
    >
      <v-card outlined>
        <v-simple-table class="elevation-1">
          <template v-slot:default>
            <tbody>
            <tr>
              <td>{{ $t('label.created_at') }}</td>
              <td>{{ createdAt }}</td>
            </tr>
            <tr>
              <td>{{ $t('label.updated_at') }}</td>
              <td>{{ updatedAt }}</td>
            </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
    </left-title>

    <v-alert outlined prominent type="error" class="ma-4">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('label.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hint.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('label.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script lang="ts">
import {Component, Prop, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import FormGroup, {GroupItem} from '@/components/FormGroup.vue';
import {GroupA, UpdateGroupQ} from '@/packet/group';
import * as _ from 'lodash';

@Component({
  components: {
    LeftTitle,
    FormGroup,
  }
})
export default class FormGroupEdit extends VueBase {
  @Prop({type: Object})
  readonly value!: GroupA;

  @Prop({type: Boolean, default: false})
  readonly showDeleteDialog!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingSubmit!: boolean;

  current = new GroupItem();
  original = new GroupItem();
  modified = false;

  get createdAt() {
    return this.value?.created_at || '';
  }

  get updatedAt() {
    return this.value?.updated_at || '';
  }

  @Watch('value')
  onChangeValue(newVal: GroupA) {
    this.updateGroup(newVal);
  }

  updateGroup(group: GroupA) {
    const slug = group?.slug || '';
    const name = group?.name || '';
    const description = group?.description || '';
    const features = group?.features || [];
    const visibility = group?.visibility || 0;

    this.current.slug = slug;
    this.current.name = name;
    this.current.description = description;
    this.current.features = features;
    this.current.visibility = visibility;
    this.original.fromObject(this.current);
    this.modified = !_.isEqual(this.original, this.current);
  }

  onUpdateCurrent(value: GroupItem) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  @Emit('ok')
  onClickOk(event: GroupItem) {
    return {
      name: event.name,
      description: event.description,
      features: event.features,
      visibility: event.visibility,
    } as UpdateGroupQ;
  }

  @Emit('delete:show')
  onClickDelete() {
    // EMPTY
  }

  @Emit('delete:cancel')
  onClickDeleteCancel() {
    // EMPTY
  }

  @Emit('delete:ok')
  onClickDeleteOk() {
    // EMPTY
  }
}
</script>
