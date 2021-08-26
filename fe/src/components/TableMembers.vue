<i18n lang="yaml">
en:
  label:
    search: "You can filter by name or description."
  headers:
    username: "Username"
    permission: "Permission"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty Members"

ko:
  label:
    search: "이름 또는 설명을 필터링할 수 있습니다."
  headers:
    username: "사용자명"
    permission: "권한"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "회원이 존재하지 않습니다."
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

    <template v-slot:item.permission="{ item }">
      <div class="d-flex justify-center">
        <v-select
            class="permission-select"
            dense
            solo
            flat
            outlined
            hide-details
            :disabled="item.permission === owner"
            v-model="item.permission"
            :items="permissions"
            @change="change($event, item)"
        ></v-select>
      </div>
    </template>

    <template v-if="!hideActions" v-slot:item.actions="{ item }">
      <v-icon
          v-if="!hideActionDelete && item.permission !== owner"
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
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {MemberA, UpdateMemberQ} from '@/packet/member';
import {PERMISSION_NAME_OWNER} from '@/packet/permission';

@Component
export default class TableMembers extends VueBase {
  private readonly owner = PERMISSION_NAME_OWNER;

  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Array, default: () => new Array<MemberA>()})
  readonly items!: Array<MemberA>;

  @Prop({type: Array, default: () => new Array<string>()})
  readonly permissions!: Array<string>;

  headers = [] as Array<object>;
  filter = '';

  created() {
    if (this.hideActions) {
      this.headers = this.createHeaders(false);
    } else {
      this.headers = this.createHeaders(true);
    }
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
        text: this.$t('headers.permission').toString(),
        align: 'center',
        filterable: true,
        sortable: true,
        value: 'permission',
      },
    ];
    if (includeActions) {
      headers.push({
        text: this.$t('headers.actions').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        value: 'actions',
      })
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

  @Emit('click:row')
  clickRow(item: MemberA) {
    return item;
  }

  @Emit()
  change(event: string, item: MemberA) {
    return {
      username: item.username,
      permission: event,
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

.permission-select {
  max-width: 140px;
}
</style>
