<i18n lang="yaml">
en:
  position:
    builtin: "Builtin"
    package: "Package"
    storage: "Storage"
  search_label: "You can filter by category or name."
  headers:
    position: "Position"
    category: "Category"
    name: "Name"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_lamdas: "Empty Lamdas"

ko:
  position:
    builtin: "내장"
    package: "패키지"
    storage: "저장소"
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

    <v-tabs v-model="tabIndex">
      <v-tab>{{ $t('position.builtin') }}</v-tab>
      <v-tab>{{ $t('position.package') }}</v-tab>
      <v-tab>{{ $t('position.storage') }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>

    <v-data-table
        :items-per-page="itemsPerPage"
        :headers="headers"
        :items="currentLamdas"
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
            small
            disabled
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
import {Component, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import {TemplateA} from '@/packet/template';
import * as _ from 'lodash';

const ITEMS_PER_PAGE = 15;
const BUILTIN_TAB_INDEX = 0;
const PACKAGE_TAB_INDEX = 1;
const STORAGE_TAB_INDEX = 2;

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class MainAdminLamdas extends VueBase {
  private readonly itemsPerPage = ITEMS_PER_PAGE;
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
      text: this.$t('headers.category').toString(),
      align: 'center',
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

  tabIndex = 0;
  filterText = '';
  totalLamdas: Array<TemplateA> = [];
  currentLamdas: Array<TemplateA> = [];
  showLoading = true;

  editCandidateKey = '';
  editCandidateValue = '';
  showEditConfigDialog = false;

  @Watch('tabIndex')
  onChangeTab(value: number) {
    this.updateCurrentLamdas(value)
  }

  mounted() {
    this.updateLamdas();
  }

  updateLamdas() {
    this.showLoading = true;
    this.$api2.getTemplates()
        .then(lamdas => {
          this.totalLamdas = lamdas;
          this.showLoading = false;
          this.updateCurrentLamdasWithTabIndex();
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  isPositionIndex(index: number) {
    switch (index) {
      case BUILTIN_TAB_INDEX:
      case PACKAGE_TAB_INDEX:
      case STORAGE_TAB_INDEX:
        return true;
      default:
        return false;
    }
  }

  updateCurrentLamdas(position: number) {
    if (!this.isPositionIndex(position)) {
      throw Error(`Unknown tab index: ${position}`)
    }
    this.currentLamdas = _.filter(this.totalLamdas, o => {
      return o.position == position;
    });
  }

  updateCurrentLamdasWithTabIndex() {
    this.updateCurrentLamdas(this.tabIndex);
  }

  onClickEditConfig(item) {
    this.editCandidateKey = item.key;
    this.editCandidateValue = item.value;
    this.showEditConfigDialog = true;
  }
}
</script>
