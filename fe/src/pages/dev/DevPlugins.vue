<i18n lang="yaml">
en:
  labels:
    search: 'You can filter by plugin name.'
  headers:
    name: 'Name'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Empty Plugin'

ko:
  labels:
    search: '플러그인 이름을 필터링할 수 있습니다.'
  headers:
    name: '이름'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '플러그인이 존재하지 않습니다.'
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
import {PluginA} from '@recc/api/dist/packet/plugin';

@Component({
  components: {
    ToolbarBreadcrumbs,
  },
})
export default class DevPlugins extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Dev',
      disabled: false,
      href: () => this.moveToDev(),
    },
    {
      text: 'Plugins',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.name'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'name',
    },
  ];

  loading = false;
  items = [] as Array<PluginA>;
  filter = '';

  created() {
    this.updatePlugins();
  }

  updatePlugins() {
    this.loading = true;
    this.$api2
      .getDevPlugins()
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
