<i18n lang="yaml">
en:
  search_label: "You can filter by category or name."
  headers:
    position: "Position"
    category: "Category"
    name: "Name"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_lamdas: "Empty Lamdas"

ko:
  search_label: "범주 또는 이름을 필터링할 수 있습니다."
  headers:
    position: "위치"
    category: "범주"
    name: "이름"
    actions: "관리"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_lamdas: "람다가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="lamdas"
        :search="filterText"
        :loading="showLoading"
        :loading-text="$t('loading')"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-text-field
              class="mr-4"
              v-model="filterText"
              append-icon="mdi-magnify"
              :label="$t('search_label')"
              single-line
              hide-details
          ></v-text-field>
        </v-toolbar>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
            v-if="false"
            small
            class="mr-2"
            @click="onClickEditConfig(item)"
        >
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_lamdas') }}
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class MainAdminLamdas extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Lamdas',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.position').toString(),
      filterable: true,
      value: 'position',
    },
    {
      text: this.$t('headers.category').toString(),
      filterable: true,
      value: 'category',
    },
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    },
  ];

  filterText = '';
  lamdas: object = [];
  showLoading = true;

  editCandidateKey = '';
  editCandidateValue = '';
  showEditConfigDialog = false;

  mounted() {
    this.updateLamdas();
  }

  updateLamdas() {
    this.showLoading = true;
    this.$api2.getTemplates()
        .then((lamdas) => {
          this.lamdas = lamdas;
          this.showLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  onClickEditConfig(item) {
    this.editCandidateKey = item.key;
    this.editCandidateValue = item.value;
    this.showEditConfigDialog = true;
  }
}
</script>
