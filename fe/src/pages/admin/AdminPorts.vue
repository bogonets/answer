<i18n lang="yaml">
en:
  titles:
    port_range: 'Port range'
  subtitles:
    port_range: 'The range in which the port can be specified.'
  labels:
    search: 'You can filter by port name.'
    add: 'Add Port'
    port_range: 'Port range'
    port_begin: 'Port Begin'
    port_end: 'Port End'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Not exists allocated port.'
  headers:
    number: 'Number'
    sock: 'Sock Type'
    ref_uid: ' Ref. UID'
    ref_category: ' Ref. Category'
    actions: 'Actions'

ko:
  titles:
    port_range: '포트 범위'
  subtitles:
    port_range: '포트를 지정할 수 있는 범위'
  labels:
    search: '포트 이름을 필터링할 수 있습니다.'
    add: '포트 추가'
    port_range: '포트 범위'
    port_begin: '시작 포트 번호'
    port_end: '종료 포트 번호'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '할당된 포트가 없습니다.'
  headers:
    number: '포트 번호'
    sock: '소켓 종류'
    ref_uid: 'UID 참조'
    ref_category: '분류 참조'
    actions: '관리'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title
      class="mt-2"
      x-small
      no-gutter
      no-wrap-xs
      :left-ratio="4"
      :right-ratio="8"
      :header="$t('titles.port_range')"
      :subheader="$t('subtitles.port_range')"
    >
      <div class="d-flex flex-row justify-end">
        <v-text-field
          class="mr-2"
          disabled
          dense
          rounded
          outlined
          readonly
          hide-details
          v-model="portMinText"
          :label="$t('labels.port_begin')"
        ></v-text-field>
        <span class="mr-2 text-subtitle-1 text--secondary">~</span>
        <v-text-field
          disabled
          dense
          rounded
          outlined
          readonly
          hide-details
          v-model="portMaxText"
          :label="$t('labels.port_end')"
        ></v-text-field>
      </div>
    </left-title>

    <v-data-table
      item-key="number"
      sort-by="number"
      sort-desc
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
              single-line
              hide-details
              :label="$t('labels.search')"
            ></v-text-field>
          </v-toolbar>
        </div>
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
import LeftTitle from '@/components/LeftTitle.vue';
import type {PortA} from '@recc/api/dist/packet/port';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
  },
})
export default class AdminPorts extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Ports',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.number'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'number',
    },
    {
      text: this.$t('headers.sock'),
      align: 'center',
      filterable: true,
      sortable: false,
      value: 'sock',
    },
    {
      text: this.$t('headers.ref_uid'),
      align: 'center',
      filterable: true,
      sortable: false,
      value: 'ref_uid',
    },
    {
      text: this.$t('headers.ref_category'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'ref_category',
    },
  ];

  loading = false;
  portMin = 0;
  portMax = 0;
  portMinText = '';
  portMaxText = '';

  items = [] as Array<PortA>;
  filter = '';

  created() {
    this.loading = true;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    try {
      this.items = await this.$api2.getAdminPorts();
      const range = await this.$api2.getAdminPortRange();
      this.portMin = range.min;
      this.portMax = range.max;
      this.portMinText = range.min.toString();
      this.portMaxText = range.max.toString();
    } catch (error) {
      this.portMin = 0;
      this.portMax = 0;
      this.portMinText = '';
      this.portMaxText = '';
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }
}
</script>
