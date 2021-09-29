<i18n lang="yaml">
en:
  groups: "Groups"
  devices: "Devices"
  service: "Service"
  labels:
    search: "You can filter by author or description."
    as_new: "New A/S"
    device: "Please select a device ID to output as a chart"
  headers:
    airjoy_name: "Name"
    airjoy_uid: "ID"
    author: "Author"
    description: "Description"
    datetime: "Datetime"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty A/S"
  add_service:
    title: "Register a new service"
    subtitle: "You can register service details"
  edit_service:
    title: "Edit a service"
    subtitle: "You can modify the contents of the service"
  delete_service:
    title: "Remove a service"
    subtitle: "Are you sure? Are you really removing this service?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  groups: "Groups"
  devices: "Devices"
  service: "Service"
  labels:
    search: "담당자 또는 기록을 필터링할 수 있습니다."
    as_new: "새로운 A/S 기록"
    device: "차트로 출력할 장치 ID를 선택하세요"
  headers:
    airjoy_name: "이름"
    airjoy_uid: "ID"
    author: "담당자"
    description: "기록"
    datetime: "날짜"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "A/S 기록이 존재하지 않습니다."
  add_service:
    title: "새로운 A/S 등록"
    subtitle: "서비스 내용을 등록할 수 있습니다"
  edit_service:
    title: "A/S 편집"
    subtitle: "서비스 내용을 수정할 수 있습니다"
  delete_service:
    title: "A/S 제거"
    subtitle: "이 서비스를 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-card>
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
            <v-btn color="primary" @click="onClickNewAs">
              {{ $t('labels.as_new') }}
            </v-btn>
          </v-toolbar>
        </template>

        <template v-slot:item.time="{ item }">
          {{ utcToDate(item.time) }}
        </template>

        <template v-if="!hideActions" v-slot:item.actions="{ item }">
          <v-icon v-if="!hideActionEdit" small class="mr-2" @click.stop="onClickServiceEdit(item)">
            mdi-pencil
          </v-icon>
          <v-icon v-if="!hideActionMove" small color="red" @click.stop="onClickServiceDelete(item)">
            mdi-delete
          </v-icon>
        </template>

        <template v-slot:no-data>
          {{ $t('msg.empty') }}
        </template>
      </v-data-table>

      <!-- Add Dialog -->
      <v-dialog
          v-model="showAddDialog"
          persistent
          no-click-animation
          :max-width="widthDialog"
          @keydown.esc.stop="onClickAddCancel"
      >
        <airjoy-service-card
            :title="$t('add_service.title')"
            :subtitle="$t('add_service.subtitle')"
            :submit-loading="loadingAddDevice"
            :devices="devices"
            @cancel="onClickAddCancel"
            @ok="onClickAddOk"
        ></airjoy-service-card>
      </v-dialog>

      <!-- Edit Dialog -->
      <v-dialog
          v-model="showEditDialog"
          persistent
          no-click-animation
          :max-width="widthDialog"
          @keydown.esc.stop="onClickEditCancel"
      >
        <airjoy-service-card
            disable-device
            :title="$t('edit_service.title')"
            :subtitle="$t('edit_service.subtitle')"
            :submit-loading="loadingEditDevice"
            :devices="devices"
            :service="editService"
            @cancel="onClickEditCancel"
            @ok="onClickEditOk"
        ></airjoy-service-card>
      </v-dialog>

      <!-- Delete dialog. -->
      <v-dialog v-model="showDeleteDialog" :max-width="widthDialog">
        <v-card>
          <v-card-title class="text-h5 error--text">
            {{ $t('delete_service.title') }}
          </v-card-title>
          <v-card-text>
            {{ $t('delete_service.subtitle') }}
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

    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import type {ServiceInfo} from '@/pages/external/airjoy/components/AirjoyServiceCard.vue';
import AirjoyServiceCard from '@/pages/external/airjoy/components/AirjoyServiceCard.vue';
import type {
  AirjoyDeviceA,
  AirjoyServiceA,
  UpdateAirjoyServiceQ,
  CreateAirjoyServiceQ,
} from '@/packet/airjoy';
import {
  UNKNOWN_ROUTE_PARAMS_DEVICE,
  createEmptyAirjoyServiceA,
} from '@/packet/airjoy';

@Component({
  components: {
    ToolbarBreadcrumbs,
    AirjoyServiceCard,
  }
})
export default class MainAirjoyService extends VueBase {
  private readonly breadcrumbs = [
    {
      text: this.$t('groups'),
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
    },
    {
      text: this.$t('devices'),
      disabled: false,
      href: () => this.moveToMainAirjoyDevices(),
    },
    {
      text: this.$t('service'),
      disabled: true,
    },
    {
      text: this.$route.params.device,
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.airjoy_name'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'airjoy_name',
      width: '128px',
    },
    {
      text: this.$t('headers.airjoy_uid'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'airjoy_uid',
      width: '128px',
    },
    {
      text: this.$t('headers.author'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'author',
      width: '128px',
    },
    {
      text: this.$t('headers.description'),
      align: 'left',
      filterable: true,
      sortable: true,
      value: 'description',
    },
    {
      text: this.$t('headers.datetime'),
      align: 'center',
      filterable: false,
      sortable: true,
      value: 'time',
      width: '128px',
    },
    {
      text: this.$t('headers.actions'),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
      width: '96px',
    }
  ];

  @Prop({type: Boolean, default: false})
  readonly hideActionEdit!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionMove!: boolean;

  @Prop({type: Number, default: 480})
  readonly widthDialog!: number;

  devices = [] as Array<AirjoyDeviceA>;
  loadingDevices = false;

  items = [] as Array<AirjoyServiceA>;
  loading = false;
  filter = '';

  showAddDialog = false;
  loadingAddDevice = false;

  showEditDialog = false;
  loadingEditDevice = false;
  editService = createEmptyAirjoyServiceA();

  showDeleteDialog = false;
  loadingDelete = false;
  deleteService = createEmptyAirjoyServiceA();

  created() {
    if (!!this.$route.params.device && this.$route.params.device !== UNKNOWN_ROUTE_PARAMS_DEVICE) {
      this.filter = this.$route.params.device;
    }
    this.updateDevices();
    this.updateServices();
  }

  updateDevices() {
    this.loadingDevices = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyDevices(group, project)
        .then(items => {
          this.loadingDevices = false;
          this.devices = items;
        })
        .catch(error => {
          this.loadingDevices = false;
          this.toastRequestFailure(error);
        });
  }

  updateServices() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2.getAirjoyServices(group, project)
        .then(items => {
          this.items = items;
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  get hideActions(): boolean {
    return this.hideActionEdit && this.hideActionMove;
  }

  utcToDate(utc?: string) {
    return utc?.split('T')[0] || '';
  }

  onChangeDevice(item: AirjoyDeviceA) {
    console.dir(item);
  }

  onClickNewAs() {
    this.showAddDialog = true;
  }

  onClickAddDevice() {
    this.showAddDialog = true;
  }

  onClickAddCancel() {
    this.showAddDialog = false;
  }

  onClickAddOk(item: ServiceInfo) {
    this.loadingAddDevice = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {
      author: item.author,
      description: item.description,
      time: item.time,
    } as CreateAirjoyServiceQ;
    this.$api2.postAirjoyServices(group, project, item.uid.toString(), body)
        .then(() => {
          this.loadingAddDevice = false;
          this.showAddDialog = false;
          this.updateServices();
        })
        .catch(error => {
          this.loadingAddDevice = false;
          this.toastRequestFailure(error);
        })
  }

  onClickServiceEdit(item: AirjoyServiceA) {
    this.editService = item;
    this.showEditDialog = true;
  }

  onClickServiceDelete(item: AirjoyServiceA) {
    this.deleteService = item;
    this.showDeleteDialog = true;
  }

  onClickEditCancel() {
    this.showEditDialog = false;
  }

  onClickEditOk(item: ServiceInfo) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.editService.airjoy_uid.toString();
    const service = this.editService.service_uid.toString();
    const body = {
      author: item.author,
      description: item.description,
      time: item.time,
    } as UpdateAirjoyServiceQ;
    this.loadingEditDevice = true;
    this.$api2.patchAirjoyServices(group, project, device, service, body)
        .then(() => {
          this.loadingEditDevice = false;
          this.showEditDialog = false;
          this.updateServices();
        })
        .catch(error => {
          this.loadingEditDevice = false;
          this.toastRequestFailure(error);
        });
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    this.loadingDelete = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.deleteService.airjoy_uid.toString();
    const service = this.deleteService.service_uid.toString();
    this.$api2.deleteAirjoyServices(group, project, device, service)
        .then(() => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.updateServices();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>

<style lang="scss" scoped>
.row-pointer {
  cursor: pointer;
}
</style>
