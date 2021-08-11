<i18n lang="yaml">
en:
  title: "Settings"
  subtitle: "Modify environment variables used in the system."
  search_label: "You can filter by key or value."
  new_info: "New info"
  headers:
    key: "Key"
    value: "Value"
    created_at: "Created at"
    updated_at: "Updated at"
    actions: "Actions"
  msg:
    request_successful: "The request was successful."
    request_failed: "Request failed."
  loading: "Loading... Please wait"
  empty_infos: "Empty Infos"

ko:
  title: "환경설정"
  subtitle: "시스템에서 사용되는 환경변수를 수정합니다."
  search_label: "열쇠 또는 값을 필터링할 수 있습니다."
  new_info: "설정 추가"
  headers:
    key: "열쇠 (Key)"
    value: "값 (Value)"
    created_at: "생성일"
    updated_at: "수정일"
    actions: "관리"
  msg:
    request_successful: "요청이 성공했습니다."
    request_failed: "요청이 실패하였습니다."
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_infos: "정보가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="infos"
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

          <v-dialog
              v-model="showNewInfoDialog"
              persistent
              max-width="360px"
              no-click-animation
              @keydown.esc.stop="onClickNewInfoCancel"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn v-bind="attrs" v-on="on" color="primary" @click="onClickAddInfo">
                {{ $t('new_info') }}
              </v-btn>
            </template>
            <card-info-new
                @cancel="onClickNewInfoCancel"
                @ok="onClickNewInfoOk"
            ></card-info-new>
          </v-dialog>

        </v-toolbar>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ utcToDate(item.created_at) }}
      </template>

      <template v-slot:item.updated_at="{ item }">
        {{ utcToDate(item.updated_at) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
            v-if="!validModifiable(item.key)"
            small
            class="mr-2"
            :disabled="validModifiable(item.key)"
            @click="onClickEditInfo(item)"
        >
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_infos') }}
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import CardInfoNew from '@/components/CardInfoNew.vue';
import {UpdateInfo} from '@/apis/api-v2';

const RECC_REGEX = /^recc\..*/;

@Component({
  components: {
    ToolbarNavigation,
    CardInfoNew: CardInfoNew,
  }
})
export default class MainAdminEnvs extends VueBase {
  private readonly snackbarTimeout = 4000;
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Settings',
      disabled: true,
    },
  ];
  private readonly headers = [
    {
      text: this.$t('headers.key').toString(),
      align: 'start',
      filterable: true,
      value: 'key',
    },
    {
      text: this.$t('headers.value').toString(),
      filterable: true,
      value: 'value',
    },
    {
      text: this.$t('headers.created_at').toString(),
      align: 'center',
      filterable: false,
      value: 'created_at',
    },
    {
      text: this.$t('headers.updated_at').toString(),
      align: 'center',
      filterable: false,
      value: 'updated_at',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    },
  ]

  filterText = '';
  infos: object = [];
  showNewInfoDialog = false;
  showLoading = true;

  mounted() {
    this.updateInfos();
  }

  updateInfos() {
    this.showLoading = true;
    this.$api2.getInfos()
        .then((infos) => {
          this.infos = infos;
          this.showLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  utcToDate(utc: undefined | string): string {
    return utc?.split('T')[0] || '';
  }

  validModifiable(key: string): boolean {
    return !!RECC_REGEX.exec(key);
  }

  validRemovable(key: string): boolean {
    return !!RECC_REGEX.exec(key);
  }

  onClickAddInfo() {
  }

  onClickEditInfo(item) {
  }

  onClickNewInfoCancel() {
    this.showNewInfoDialog = false;
  }

  onClickNewInfoOk(event) {
    this.showNewInfoDialog = false;

    const info = {
      key: event.key,
      value: event.value,
    } as UpdateInfo;
    this.$api2.postInfos(info)
        .then(() => {
          this.updateInfos();
          this.$toast.info(this.$t('msg.request_successful').toString());
        })
        .catch(error => {
          const code = error.request.status;
          const reason = error.request.statusText;
          console.error(`Request failed: code=${code}, reason=${reason}`);
          this.$toast.error(this.$t('msg.request_failed').toString());
        });
  }
}
</script>
