<i18n lang="yaml">
en:
  headers:
    key: 'ID'
    name: 'Name'
    image: 'Image'
    created: 'Created'
    status: 'Status'
    actions: 'Actions'
  sync: 'Sync'
  search_label: 'You can filter by key or name.'
  loading: 'Loading... Please wait'
  empty_items: 'Empty Containers'
  no_selected: 'There are no items selected.'

ko:
  headers:
    key: 'ID'
    name: '이름'
    image: '이미지'
    created: '생성일'
    status: '상태'
    actions: '관리'
  sync: '동기화'
  search_label: '키(Key) 또는 이름을 필터링할 수 있습니다.'
  loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
  empty_items: '컨테이너가 존재하지 않습니다.'
  no_selected: '선택된 항목이 없습니다.'
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Tasks"></breadcrumb-main>
    <v-divider></v-divider>

    <v-data-table
      :value="selected"
      @input="onInputSelected"
      show-select
      item-key="key"
      :items-per-page="itemsPerPage"
      :headers="headers"
      :items="items"
      :search="filter"
      :loading="loading"
      :loading-text="$t('loading')"
    >
      <template v-slot:top>
        <div>
          <v-toolbar flat>
            <v-text-field
              class="mr-4"
              v-model="filter"
              append-icon="mdi-magnify"
              :label="$t('search_label')"
              single-line
              hide-details
            ></v-text-field>
          </v-toolbar>
        </div>
        <div class="d-flex flex-row">
          <container-control-group
            small
            :disabled-start="disabledStart"
            :disabled-stop="disabledStop"
            :disabled-kill="disabledKill"
            :disabled-restart="disabledRestart"
            :disabled-pause="disabledPause"
            :disabled-resume="disabledResume"
            :disabled-remove="disabledRemove"
            @click:start="onClickStart"
            @click:stop="onClickStop"
            @click:kill="onClickKill"
            @click:restart="onClickRestart"
            @click:pause="onClickPause"
            @click:resume="onClickResume"
            @click:remove="onClickRemove"
          ></container-control-group>
          <v-btn
            class="ml-2 rounded-xl"
            color="primary"
            small
            outlined
            rounded
            tile
            @click="onClickSync"
          >
            <v-icon left>mdi-sync</v-icon>
            {{ $t('sync') }}
          </v-btn>
        </div>
      </template>

      <template v-slot:item.key="{item}">
        {{ shortKey(item) }}
      </template>

      <template v-slot:item.image="{item}">
        {{ shortImage(item) }}
      </template>

      <template v-slot:item.created="{item}">
        {{ shortCreated(item) }}
      </template>

      <template v-slot:item.status="{item}">
        <v-chip small :color="statusColor(item)">
          {{ item.status }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{item}">
        <v-icon small disabled class="mr-2" @click="onClickContainerEdit(item)">
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_items') }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import ContainerControlGroup from '@/components/ContainerControlGroup.vue';
import type {ContainerA, ControlContainersQ} from '@recc/api/dist/packet/container';
import {
  STATUS_CREATED,
  STATUS_RESTARTING,
  STATUS_RUNNING,
  STATUS_REMOVING,
  STATUS_PAUSED,
  STATUS_EXITED,
  STATUS_DEAD,
  CONTROL_OPERATOR_START,
  CONTROL_OPERATOR_STOP,
  CONTROL_OPERATOR_KILL,
  CONTROL_OPERATOR_RESTART,
  CONTROL_OPERATOR_PAUSE,
  CONTROL_OPERATOR_RESUME,
  CONTROL_OPERATOR_REMOVE,
} from '@recc/api/dist/packet/container';
import {iso8601ToLocalDate} from '@/chrono/iso8601';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    BreadcrumbMain,
    ContainerControlGroup,
  },
})
export default class MainTasks extends VueBase {
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly headers = [
    {
      text: this.$t('headers.key').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      width: '130px',
      value: 'key',
    },
    {
      text: this.$t('headers.image').toString(),
      align: 'center',
      filterable: false,
      sortable: true,
      width: '130px',
      value: 'image',
    },
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.created').toString(),
      align: 'center',
      filterable: false,
      sortable: true,
      value: 'created',
    },
    {
      text: this.$t('headers.status').toString(),
      align: 'center',
      filterable: false,
      sortable: true,
      width: '100px',
      value: 'status',
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
  filter = '';
  items = [] as Array<ContainerA>;
  selected = [] as Array<ContainerA>;
  disabledStart = true;
  disabledStop = true;
  disabledKill = true;
  disabledRestart = true;
  disabledPause = true;
  disabledResume = true;
  disabledRemove = true;

  created() {
    this.updateContainers();
  }

  updateContainers() {
    this.loading = true;
    this.$api2
      .getAdminContainers()
      .then(items => {
        this.loading = false;
        this.items = items;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  shortKey(item: ContainerA) {
    return item.key.substring(0, 12);
  }

  shortImage(item: ContainerA) {
    if (item.image.substring(0, 7) === 'sha256:') {
      return item.image.substring(7, 19);
    } else {
      return item.image.substring(0, 12);
    }
  }

  shortCreated(item: ContainerA) {
    return iso8601ToLocalDate(item.created);
  }

  statusColor(item: ContainerA) {
    if (item.status === STATUS_CREATED) {
      return 'blue';
    } else if (item.status === STATUS_RESTARTING) {
      return 'blue';
    } else if (item.status === STATUS_RUNNING) {
      return 'green';
    } else if (item.status === STATUS_REMOVING) {
      return 'orange';
    } else if (item.status === STATUS_PAUSED) {
      return 'blue';
    } else if (item.status === STATUS_EXITED) {
      return 'grey';
    } else if (item.status === STATUS_DEAD) {
      return 'red';
    } else {
      return 'black';
    }
  }

  onClickContainerEdit(item: ContainerA) {}

  onInputSelected(value) {
    this.selected = value;
    if (this.selected.length == 0) {
      this.disabledStart = true;
      this.disabledStop = true;
      this.disabledKill = true;
      this.disabledRestart = true;
      this.disabledPause = true;
      this.disabledResume = true;
      this.disabledRemove = true;
    } else {
      this.disabledStart = false;
      this.disabledStop = false;
      this.disabledKill = false;
      this.disabledRestart = false;
      this.disabledPause = false;
      this.disabledResume = false;
      this.disabledRemove = false;
    }
  }

  onClickSync() {
    this.updateContainers();
  }

  controlContainers(operator: string) {
    const keys = this.selected.map(i => i.key);
    if (keys.length === 0) {
      this.toastError(this.$t('no_selected').toString());
      return;
    }

    const body = {
      keys: keys,
      operator: operator,
    } as ControlContainersQ;

    this.$api2
      .patchAdminContainers(body)
      .then(() => {
        this.selected = [];
        this.updateContainers();
        this.toastRequestSuccess();
      })
      .catch(error => {
        this.selected = [];
        this.updateContainers();
        this.toastRequestFailure(error);
      });
  }

  onClickStart() {
    this.controlContainers(CONTROL_OPERATOR_START);
  }

  onClickStop() {
    this.controlContainers(CONTROL_OPERATOR_STOP);
  }

  onClickKill() {
    this.controlContainers(CONTROL_OPERATOR_KILL);
  }

  onClickRestart() {
    this.controlContainers(CONTROL_OPERATOR_RESTART);
  }

  onClickPause() {
    this.controlContainers(CONTROL_OPERATOR_PAUSE);
  }

  onClickResume() {
    this.controlContainers(CONTROL_OPERATOR_RESUME);
  }

  onClickRemove() {
    this.controlContainers(CONTROL_OPERATOR_REMOVE);
  }
}
</script>
