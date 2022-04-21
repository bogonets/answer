<i18n lang="yaml">
en:
  labels:
    delete: 'Delete a config'
  msg:
    delete_confirm: 'Are you sure? Are you really removing this config?'
  cancel: 'Cancel'
  delete: 'Delete'

ko:
  labels:
    delete: '설정 제거'
  msg:
    delete_confirm: '이 설정을 정말 제거합니까?'
  cancel: '취소'
  delete: '제거'
</i18n>

<template>
  <div>
    <table-vms-event-configs
      :items="items"
      :loading="loading"
      @click:new="onClickEventConfigNew"
      @click:active="onClickEventConfigItemActive"
      @click:edit="onClickEventConfigEdit"
      @click:delete="onClickEventConfigDelete"
    ></table-vms-event-configs>

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
          <v-btn @click="onClickEventConfigDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
            color="error"
            :loading="loadingDelete"
            @click="onClickEventConfigDeleteOk"
          >
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
import TableVmsEventConfigs from '@/components/TableVmsEventConfigs.vue';
import type {VmsEventConfigA, VmsUpdateEventConfigQ} from '@/packet/vms';

@Component({
  components: {
    TableVmsEventConfigs,
  },
})
export default class MainVmsDevicesEditEvents extends VueBase {
  loading = false;
  items = [] as Array<VmsEventConfigA>;

  showDeleteDialog = false;
  loadingDelete = false;
  eventConfigCandidate = 0;

  created() {
    this.requestEventConfigs();
  }

  requestEventConfigs() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    this.loading = true;
    this.$api2
      .getVmsDeviceEventsConfigs(group, project, device)
      .then(items => {
        this.loading = false;
        this.items = items;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickEventConfigNew() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.moveToMainVmsDevicesEditEventConfigsNew(group, project, device);
  }

  onClickEventConfigItemActive(item: VmsEventConfigA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const config = item.event_config_uid.toString();
    const updateEnableFlag = !item.enable;
    const body = {
      enable: updateEnableFlag,
    } as VmsUpdateEventConfigQ;
    this.$api2
      .patchVmsDeviceEventsConfigsPconfig(group, project, device, config, body)
      .then(() => {
        item.enable = updateEnableFlag;
        this.toastRequestSuccess();
      })
      .catch(error => {
        this.toastRequestFailure(error);
      });
  }

  onClickEventConfigEdit(item: VmsEventConfigA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const config = item.event_config_uid.toString();
    this.moveToMainVmsDevicesEditEventConfigsEdit(group, project, device, config);
  }

  onClickEventConfigDelete(item: VmsEventConfigA) {
    this.showDeleteDialog = true;
    this.eventConfigCandidate = item.event_config_uid;
  }

  onClickEventConfigDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickEventConfigDeleteOk() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const config = this.eventConfigCandidate.toString();

    this.loadingDelete = true;
    this.$api2
      .deleteVmsDeviceEventsConfigsPconfig(group, project, device, config)
      .then(() => {
        this.showDeleteDialog = false;
        this.loadingDelete = false;
        this.toastRequestSuccess();
        this.requestEventConfigs();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
