<i18n lang="yaml">
en:
  layouts: "Layouts"
  headers:
    name: "Name"
    index: "Index"
    device_uid: "Device UID"
    actions: "Actions"
  msg:
    search: "You can filter by name."
    loading: "Loading... Please wait"
    empty: "Empty Layouts"
  labels:
    add: "Add Layout"

ko:
  layouts: "Layouts"
  headers:
    name: "이름"
    index: "배치 순서"
    device_uid: "장치 UID"
    actions: "관리"
  msg:
    search: "이름을 필터링할 수 있습니다."
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "레이아웃이 존재하지 않습니다."
  labels:
    add: "레이아웃 추가"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
        :items-per-page="itemsPerPage"
        :headers="headers"
        :items="items"
        :search="filter"
        :loading="loading"
        :loading-text="$t('msg.loading')"
    >
      <template v-slot:top>
        <div>
          <v-toolbar flat>
            <v-text-field
                class="mr-4"
                v-model="filter"
                append-icon="mdi-magnify"
                :label="$t('msg.search')"
                single-line
                hide-details
            ></v-text-field>

            <v-btn color="primary" class="align-self-center mr-2" @click="onClickAdd">
              {{ $t('labels.add') }}
            </v-btn>
          </v-toolbar>
        </div>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="onClickLayout(item)">
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import type {VmsDeviceA, VmsLayoutA} from '@/packet/vms';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class MainVmsLayouts extends VueBase {
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly breadcrumbs = [
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
    },
    {
      text: this.$t('layouts'),
      disabled: true,
    },
  ];

  readonly headers = [
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.index').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'index',
    },
    {
      text: this.$t('headers.device_uid').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'device_uid',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      width: '1px',
      value: 'actions',
    },
  ];

  loading = false;
  devices = [] as Array<VmsDeviceA>;
  items = [] as Array<VmsLayoutA>;
  filter = '';

  created() {
    this.requestSetup();
  }

  requestSetup() {
    this.loading = true;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;

      this.devices = await this.$api2.getVmsDevices(group, project);
      this.items = await this.$api2.getVmsLayouts(group, project);
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  onClickAdd() {
    this.moveToMainVmsLayoutsNew();
  }

  onClickLayout(item: VmsLayoutA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const layout = item.layout_uid.toString();
    this.moveToMainVmsLayoutsEdit(group, project, layout);
  }
}
</script>
