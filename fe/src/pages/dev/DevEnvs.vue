<i18n lang="yaml">
en:
  labels:
    search: "You can filter by key or value."
  headers:
    key: "Key"
    value: "Value"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty environment variables"

ko:
  labels:
    search: "열쇠 또는 값을 필터링할 수 있습니다."
  headers:
    key: "열쇠 (Key)"
    value: "값 (Value)"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "환경변수가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="items"
        :search="filter"
        :loading="loading"
        :loading-text="$t('msg.loading')"
    >
      <template v-slot:top>
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
import type {EnvironmentA} from '@/packet/environment';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class DevEnvs extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Dev',
      disabled: false,
      href: () => this.moveToDev(),
    },
    {
      text: 'Environment Variables',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.key'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'key',
    },
    {
      text: this.$t('headers.value'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'value',
    },
  ];

  loading = false;
  items = [] as Array<EnvironmentA>;
  filter = '';

  created() {
    this.updatePlugins();
  }

  updatePlugins() {
    this.loading = true;
    this.$api2.getDevEnvironments()
        .then(items => {
          this.loading = false;
          this.items = items;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
