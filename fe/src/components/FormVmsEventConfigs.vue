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
    category: "Category"
    name: "Name"
    updated_at: "Updated at"
    actions: "Actions"
  category:
    color: "Color"
    detection: "Detection"
    matching: "Matching"
    ocr: "OCR"
    unknown: "Unknown"
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
    category: "종류"
    name: "이름"
    updated_at: "수정일"
    actions: "관리"
  category:
    color: "색상 비교"
    detection: "객체 탐지"
    matching: "영상 비교"
    ocr: "문자 인식"
    unknown: "알 수 없음"
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
        <v-simple-checkbox
            :value="item.enable"
            @input="onInputEnable(item, $event)"
        ></v-simple-checkbox>
      </template>

      <template v-slot:item.category="{ item }">
        <v-chip>
          <v-icon left>{{ categoryIcon(item) }}</v-icon>
          {{ categoryText(item) }}
        </v-chip>
      </template>

      <template v-slot:item.updated_at="{ item }">
        {{ datetimeToDate(item.updated_at) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon v-show="false" small class="mr-2" @click="onClickEventEdit(item)">
          mdi-pencil
        </v-icon>
        <v-icon small class="mr-2" color="error" @click="onClickEventDelete(item)">
          mdi-delete
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>

    <!-- New dialog. -->
    <v-dialog v-model="showNewDialog" :max-width="dialogWidth">
      <!-- To release MediaPlayer memory and release debugging mode, `v-if` must be used. -->
      <card-vms-event-configs-new
          v-if="showNewDialog"
          disable-device
          :title="$t('titles.new')"
          :subtitle="$t('subtitles.new')"
          @cancel="onClickNewCancel"
          @ok="onClickNewSubmit"
      ></card-vms-event-configs-new>
    </v-dialog>

    <!-- Edit dialog. -->
    <v-dialog v-model="showEditDialog" :max-width="dialogWidth">
    </v-dialog>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="360px">
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
import CardVmsEventConfigsNew from '@/components/CardVmsEventConfigsNew.vue';
import type {
  VmsEventConfigA,
  VmsCreateEventConfigQ,
  VmsUpdateEventConfigQ,
} from '@/packet/vms';
import {
  EVENT_CATEGORY_NAME_COLOR,
  EVENT_CATEGORY_NAME_DETECTION,
  EVENT_CATEGORY_NAME_MATCHING,
  EVENT_CATEGORY_NAME_OCR,
} from '@/packet/vms';
import {iso8601ToLocalDate} from '@/chrono/iso8601';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    CardVmsEventConfigsNew,
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
      width: '80px',
      value: 'enable',
    },
    {
      text: this.$t('headers.category').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'category',
    },
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.updated_at').toString(),
      align: 'center',
      filterable: false,
      sortable: true,
      value: 'updated_at',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      width: '80px',
      value: 'actions',
    },
  ];

  readonly categories = [
    {
      icon: 'mdi-palette',
      text: this.$t('category.color'),
      value: EVENT_CATEGORY_NAME_COLOR,
    },
    {
      icon: 'mdi-image-search',
      text: this.$t('category.detection'),
      value: EVENT_CATEGORY_NAME_DETECTION,
    },
    {
      icon: 'mdi-compare',
      text: this.$t('category.matching'),
      value: EVENT_CATEGORY_NAME_MATCHING,
    },
    {
      icon: 'mdi-ocr',
      text: this.$t('category.ocr'),
      value: EVENT_CATEGORY_NAME_OCR,
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
  deleteCandidate?: VmsEventConfigA;
  loadingDelete = false;

  created() {
    this.requestItems();
  }

  requestItems() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2.getVmsEventsConfigs(group, project)
        .then(items => {
          this.loading = false;
          this.items = items;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  get dialogWidth() {
    return "80%";
  }

  datetimeToDate(text) {
    return iso8601ToLocalDate(text);
  }

  categoryIcon(item: VmsEventConfigA) {
    const findCategory = this.categories.find(i => i.value == item.category);
    if (typeof findCategory === 'undefined') {
      return '';
    }
    return findCategory.icon;
  }

  categoryText(item: VmsEventConfigA) {
    const findCategory = this.categories.find(i => i.value == item.category);
    if (typeof findCategory === 'undefined') {
      return this.$t('category.unknown').toString();
    }
    return findCategory.text;
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
    this.$api2.postVmsEventsConfigs(group, project, body)
        .then(() => {
          this.loadingNew = false;
          this.showNewDialog = false;
          this.toastRequestSuccess();
          this.requestItems();
        })
        .catch(error => {
          this.loadingNew = false;
          this.toastRequestFailure(error);
        });
  }

  onInputEnable(item: VmsEventConfigA, event) {
    // console.debug(`onInputEnable -> ${event}`)
    // console.dir(item);
    // console.dir(event);
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const config = item.event_config_uid.toString();
    const body = {
      enable: !!event,
    } as VmsUpdateEventConfigQ;
    this.$api2.patchVmsEventsConfigsPconfig(group, project, config, body)
        .then(() => {
          item.enable = !!event;
          this.toastRequestSuccess();
        })
        .catch(error => {
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
    this.deleteCandidate = item;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    if (typeof this.deleteCandidate === 'undefined') {
      throw new Error('There are no deletion candidates.');
    }

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const config = this.deleteCandidate.event_config_uid.toString();
    this.loadingDelete = true;
    this.$api2.deleteVmsEventsConfigsPconfig(group, project, config)
        .then(() => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.requestItems();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
