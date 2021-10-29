<i18n lang="yaml">
en:
  labels:
    add: "Add Event"
    delete: "Delete a Event"
  headers:
    enable: "Enable"
    type: "Type"
    name: "Name"
    actions: "Actions"
  msg:
    loading: ""
    search: ""
    unknown_event_type: ""
    empty: ""
    delete_confirm: "이 레이아웃을 정말 제거합니까?"
  cancel: "Cancel"
  submit: "Submit"
  delete: "Delete"

ko:
  labels:
    add: "이벤트 추가"
    delete: "이벤트 제거"
  headers:
    enable: "활성화"
    type: "종류"
    name: "이름"
    actions: "관리"
  msg:
    loading: ""
    search: ""
    unknown_event_type: ""
    empty: ""
    delete_confirm: "이 레이아웃을 정말 제거합니까?"
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
    <v-dialog v-model="showNewDialog" max-width="320">
      <card-vms-event-configs
      ></card-vms-event-configs>
    </v-dialog>

    <!-- Edit dialog. -->
    <v-dialog v-model="showEditDialog" max-width="320">
      <card-vms-event-configs
      ></card-vms-event-configs>
    </v-dialog>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
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
import type {VmsEventConfigA} from '@/packet/vms';
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

  showEditDialog = false;

  showDeleteDialog = false;
  loadingDelete = false;

  onClickAdd() {
    this.showNewDialog = true;
  }

  onClickEventEdit(item: VmsEventConfigA) {
    this.showEditDialog = true;
    // if (item.type == EVENT_TYPE_NAME_COLOR) {
    //   this.showColorDialog = true;
    // } else if (item.type == EVENT_TYPE_NAME_DETECTION) {
    //   this.showDetectionDialog = true;
    // } else if (item.type == EVENT_TYPE_NAME_MATCHING) {
    //   this.showMatchingDialog = true;
    // } else if (item.type == EVENT_TYPE_NAME_OCR) {
    //   this.showOcrDialog = true;
    // } else {
    //   this.toastError(this.$t('msg.unknown_event_type').toString());
    // }
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
