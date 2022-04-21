<i18n lang="yaml">
en:
  label:
    search: 'You can filter by name or description.'
    owner: 'Owner'
  headers:
    username: 'Username'
    role: 'Role'
    actions: 'Actions'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Empty Members'

ko:
  label:
    search: '이름 또는 설명을 필터링할 수 있습니다.'
    owner: '소유자'
  headers:
    username: '사용자명'
    role: '역할'
    actions: '관리'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '회원이 존재하지 않습니다.'
</i18n>

<template>
  <v-data-table
    :class="dataTableClass"
    :headers="headers"
    :items="items"
    :search="filter"
    :loading="loading"
    :loading-text="$t('msg.loading')"
    @click:row="onClickRow"
  >
    <template v-if="!hideTopBar" v-slot:top>
      <v-toolbar flat>
        <v-text-field
          v-if="!hideFilterInput"
          class="mr-4"
          v-model="filter"
          append-icon="mdi-magnify"
          single-line
          hide-details
          :label="$t('label.search')"
        ></v-text-field>
      </v-toolbar>
    </template>

    <template v-slot:item.role="{item}">
      <div class="d-flex justify-center">
        <span class="font-weight-bold" v-if="item.role === owner">
          {{ $t('label.owner') }}
        </span>
        <v-select
          v-else
          dense
          solo
          flat
          outlined
          rounded
          hide-details
          :disabled="item.role === owner"
          :value="selectPermission(item)"
          @input="inputPermission($event, item)"
          :items="visibleRoles"
          @change="change($event, item)"
          item-text="slug"
          item-value="slug"
          item-disabled="hidden"
          return-object
        >
          <template v-slot:item="{item}">
            {{ item.name }}
            <v-chip class="ml-2" x-small outlined color="primary">
              <v-icon left>mdi-identifier</v-icon>
              {{ item.slug }}
            </v-chip>
          </template>

          <template v-slot:selection="{item}">
            {{ item.name }}
            <v-chip class="ml-2" x-small outlined color="primary">
              <v-icon left>mdi-identifier</v-icon>
              {{ item.slug }}
            </v-chip>
          </template>
        </v-select>
      </div>
    </template>

    <template v-if="!hideActions" v-slot:item.actions="{item}">
      <v-icon
        v-if="!hideActionDelete && item.role !== owner"
        small
        color="red"
        @click="clickDelete(item)"
      >
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:no-data>
      {{ $t('msg.empty') }}
    </template>
  </v-data-table>
</template>

<script lang="ts">
import {Component, Prop, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {MemberA, UpdateMemberQ} from '@/packet/member';
import type {RoleA} from '@/packet/role';
import {ROLE_SLUG_OWNER} from '@/packet/role';

@Component
export default class TableMembers extends VueBase {
  readonly owner = ROLE_SLUG_OWNER;

  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Array, default: () => []})
  readonly items!: Array<MemberA>;

  @Prop({type: Array, default: () => []})
  readonly permissions!: Array<RoleA>;

  visibleRoles = [] as Array<RoleA>;
  headers = [] as Array<object>;
  filter = '';

  created() {
    if (this.hideActions) {
      this.headers = this.createHeaders(false);
    } else {
      this.headers = this.createHeaders(true);
    }
    this.updateVisiblePermissionNames();
  }

  @Watch('permissions')
  onWatchPermissions(newVal: Array<RoleA>) {
    this.updateVisiblePermissionNames();
  }

  updateVisiblePermissionNames() {
    this.visibleRoles = this.permissions.filter(x => {
      return x.slug !== this.owner && !x.hidden;
    });
  }

  get hideTopBar(): boolean {
    return this.hideFilterInput;
  }

  get hideActions(): boolean {
    return this.hideActionDelete;
  }

  createHeaders(includeActions = true) {
    const headers = [
      {
        text: this.$t('headers.username').toString(),
        align: 'center',
        filterable: true,
        sortable: true,
        value: 'username',
      },
      {
        text: this.$t('headers.role').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        value: 'role',
      },
    ];
    if (includeActions) {
      headers.push({
        text: this.$t('headers.actions').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        value: 'actions',
      });
    }
    return headers;
  }

  get dataTableClass(): string {
    if (this.items.length >= 1 && this.clickableRow) {
      return 'row-pointer';
    } else {
      return '';
    }
  }

  selectPermission(item: MemberA) {
    return this.permissions.find(p => p.slug === item.role);
  }

  inputPermission(event: RoleA, item: MemberA) {
    item.role = event.slug;
  }

  @Emit('click:row')
  clickRow(item: MemberA) {
    return item;
  }

  @Emit()
  change(event: RoleA, item: MemberA) {
    return {
      username: item.username,
      role: event.slug,
    } as UpdateMemberQ;
  }

  @Emit('click:delete')
  clickDelete(item: MemberA) {
    return item;
  }

  onClickRow(item: MemberA) {
    if (this.clickableRow) {
      this.clickRow(item);
    }
  }
}
</script>

<style lang="scss" scoped>
.row-pointer::v-deep tr {
  cursor: pointer;
}
</style>
