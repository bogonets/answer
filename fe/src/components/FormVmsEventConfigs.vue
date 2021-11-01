<i18n lang="yaml">
en:
  titles:
    new: "New Event"
  subtitles:
    new: "Set up and add a new event."
  labels:
    add: "Add Event"
    delete: "Delete a Event"
  headers:
    enable: "Enable"
    type: "Type"
    name: "Name"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    search: "You can filter by name."
    empty: "Empty Events"
    delete_confirm: "Are you really removing this event?"
  cancel: "Cancel"
  submit: "Submit"
  delete: "Delete"

ko:
  titles:
    new: "새로운 이벤트"
  subtitles:
    new: "새 이벤트를 설정하고 추가합니다."
  labels:
    add: "이벤트 추가"
    delete: "이벤트 제거"
  headers:
    enable: "활성화"
    type: "종류"
    name: "이름"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    search: "이름을 필터링할 수 있습니다."
    empty: "이벤트가 존재하지 않습니다."
    delete_confirm: "이 이벤트를 정말 제거합니까?"
  cancel: "취소"
  submit: "제출"
  delete: "제거"
</i18n>

<template>
  <div>
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

      <template v-slot:item.enable="{ item }">
        <v-icon v-show="item.enable" small disabled>
          mdi-check
        </v-icon>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="onClickEventEdit(item)">
          mdi-pencil
        </v-icon>
        <v-icon small class="mr-2" @click="onClickEventDelete(item)">
          mdi-delete
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>

    <!-- Add dialog. -->
    <v-dialog v-model="showNewDialog" :max-width="dialogWidth">
      <card-vms-event-configs
          disable-device
          :title="$t('titles.new')"
          :subtitle="$t('subtitles.new')"
          @cancel="onClickNewCancel"
          @ok="onClickNewSubmit"
      ></card-vms-event-configs>
    </v-dialog>

    <!-- Edit dialog. -->
    <v-dialog v-model="showEditDialog" :max-width="dialogWidth">
      <card-vms-event-configs
      ></card-vms-event-configs>
    </v-dialog>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" :max-width="dialogWidth">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('labels.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('msg.delete_confirm') }}
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
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {VmsCreateEventConfigQ, VmsEventConfigA} from '@/packet/vms';
import CardVmsEventConfigs from '@/components/CardVmsEventConfigs.vue';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    CardVmsEventConfigs,
  },
})
export default class FormVmsEventConfigs extends VueBase {
  readonly itemsPerPage = ITEMS_PER_PAGE;

  readonly headers = [
    {
      text: this.$t('headers.enable').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      width: '1px',
      value: 'enable',
    },
    {
      text: this.$t('headers.type').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'type',
    },
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
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
  items = [] as Array<VmsEventConfigA>;
  filter = '';

  original = {} as VmsEventConfigA;
  current = {} as VmsEventConfigA;

  showNewDialog = false;
  loadingNew = false;

  showEditDialog = false;

  showDeleteDialog = false;
  loadingDelete = false;

  get dialogWidth() {
    return "80%";
  }

  onClickAdd() {
    this.showNewDialog = true;
  }

  onClickNewCancel() {
    this.showNewDialog = false;
  }

  onClickNewSubmit(body: VmsCreateEventConfigQ) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loadingNew = true;
    console.debug(`onClickNewSubmit`);
    console.dir(body);
    this.$api2.postVmsEventsConfigs(group, project, body)
        .then(() => {
          this.loadingNew = false;
          this.showNewDialog = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.loadingNew = false;
          this.toastRequestFailure(error);
        });
  }

  onClickEventEdit(item: VmsEventConfigA) {
    this.showEditDialog = true;
  }

  onClickEventConfigCancel() {
    this.showEditDialog = false;
  }

  onClickEventConfigSubmit(item: VmsEventConfigA) {
  }

  onClickEventDelete(item: VmsEventConfigA) {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    // const group = this.$route.params.group;
    // const project = this.$route.params.project;
    // const layout = this.$route.params.layout;
    // this.loadingDelete = true;
    // this.$api2.deleteVmsLayout(group, project, layout)
    //     .then(() => {
    //       this.loadingDelete = false;
    //       this.showDeleteDialog = false;
    //       this.toastRequestSuccess();
    //       this.moveToMainVmsLayouts();
    //     })
    //     .catch(error => {
    //       this.loadingDelete = false;
    //       this.toastRequestFailure(error);
    //     });
  }
}
</script>
