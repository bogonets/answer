<i18n lang="yaml">
en:
  header:
    basic: "Edit Daemon"
    detail: "Detail"
  subheader:
    basic: "A daemon is a program that runs in the background."
    detail: "Detailed information about this daemon."
  labels:
    created_at: "Created At"
    updated_at: "Updated At"
    requirements_sha256: "Req/SHA256"
    status: "Status"
    exit_code: "Exit code"
    delete: "Delete a daemon"
  control:
    start: "Start"
    stop: "Stop"
    sync: "Sync"
  hints:
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this daemon?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    basic: "데몬 편집"
    detail: "상세 정보"
  subheader:
    basic: "데몬은 백그라운드에서 실행되는 프로그램 입니다."
    detail: "이 데몬에 대한 자세한 정보입니다."
  labels:
    created_at: "데몬 생성일"
    updated_at: "데몬 갱신일"
    requirements_sha256: "Req/SHA256"
    status: "상태"
    exit_code: "종료 코드"
    delete: "데몬 제거"
  control:
    start: "Start"
    stop: "Stop"
    sync: "Sync"
  hints:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 데몬을 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title
        :header="$t('header.basic')"
        :subheader="$t('subheader.basic')"
    >
      <form-daemon
          hide-cancel-button
          disable-plugin
          disable-slug
          :loading-plugin="loadingPlugins"
          :loading-submit="loadingSubmit"
          :disable-submit-button="!modified"
          :plugins="plugins"
          :value="current"
          @input="onUpdateCurrent"
          @ok="onClickOk"
      ></form-daemon>
    </left-title>

    <left-title
        :header="$t('header.detail')"
        :subheader="$t('subheader.detail')"
    >
      <v-card outlined>
        <v-simple-table class="elevation-1">
          <template v-slot:default>
            <tbody>
            <tr>
              <td>{{ $t('labels.created_at') }}</td>
              <td>{{ createdAt }}</td>
            </tr>
            <tr>
              <td>{{ $t('labels.updated_at') }}</td>
              <td>{{ updatedAt }}</td>
            </tr>
            <tr>
              <td>{{ $t('labels.requirements_sha256') }}</td>
              <td>{{ original.requirements_sha256 }}</td>
            </tr>
            <tr>
              <td>{{ $t('labels.status') }}</td>
              <td>
                <v-chip small :color="serverStatusColor(original.status)">
                  {{ original.status }}
                </v-chip>
              </td>
            </tr>
            <tr>
              <td>{{ $t('labels.exit_code') }}</td>
              <td>{{ original.exit_code }}</td>
            </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>

      <div class="d-flex flex-row mt-4">
        <v-btn
            class="ml-2 rounded-xl"
            color="green"
            small
            rounded
            tile
            @click="onClickStart"
        >
          <v-icon left>mdi-play</v-icon>
          {{ $t('control.start') }}
        </v-btn>
        <v-btn
            class="ml-2 rounded-xl"
            color="red"
            small
            rounded
            tile
            @click="onClickStop"
        >
          <v-icon left>mdi-stop</v-icon>
          {{ $t('control.stop') }}
        </v-btn>
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
          {{ $t('control.sync') }}
        </v-btn>
      </div>
    </left-title>

    <v-alert outlined prominent type="error" class="ma-4">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('labels.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hints.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('labels.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
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

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormDaemon from '@/components/FormDaemon.vue';
import type {DaemonA, UpdateDaemonQ} from '@/packet/daemon';
import {iso8601ToLocal} from '@/chrono/iso8601';
import * as _ from 'lodash';
import {getStatusColor, isStatusRunning} from "@/packet/daemon";

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormDaemon,
  }
})
export default class AdminDaemonsEdit extends VueBase {
  readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Daemons',
      disabled: false,
      href: () => this.moveToAdminDaemons(),
    },
    {
      text: 'Edit',
      disabled: true,
    },
    {
      text: this.$route.params.daemon,
      disabled: true,
    },
  ];

  loadingPlugins = false;
  plugins = [] as Array<string>;

  current = {} as DaemonA;
  original = {} as DaemonA;
  modified = false;
  loadingSubmit = false;

  showDeleteDialog = false;
  loadingDelete = false;

  created() {
    this.setup();
  }

  setup() {
    this.loadingPlugins = true;
    (async () => {
      await this.requestSetup();
    })();
  }

  async requestSetup() {
    try {
      this.plugins = await this.$api2.getAdminDaemonPlugins();

      const daemon = this.$route.params.daemon;
      const item = await this.$api2.getAdminDaemonsPdaemon(daemon);
      this.original = _.cloneDeep(item);
      this.current = _.cloneDeep(item);
      this.modified = false;
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loadingPlugins = false;
    }
  }

  serverStatusColor(status?: string) {
    return getStatusColor(status)
  }

  get createdAt() {
    return iso8601ToLocal(this.original?.created_at || '');
  }

  get updatedAt() {
    return iso8601ToLocal(this.original?.updated_at || '');
  }

  onUpdateCurrent(value: DaemonA) {
    this.current = _.cloneDeep(value);
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickOk(event: DaemonA) {
    const body = {
      name: event.name,
      address: event.address,
      description: event.description,
      enable: event.enable,
    } as UpdateDaemonQ;

    const daemon = this.$route.params.daemon;
    this.loadingSubmit = true;
    this.$api2.patchAdminDaemonsPdaemon(daemon, body)
        .then(() => {
          this.loadingSubmit = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.loadingSubmit = false;
          this.toastRequestFailure(error);
        });
  }

  onClickStart() {
    const daemon = this.$route.params.daemon;
    this.$api2.postAdminDaemonsPdaemonStart(daemon)
        .then(() => {
          this.toastRequestSuccess();
          this.setup();
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  onClickStop() {
    const daemon = this.$route.params.daemon;
    this.$api2.postAdminDaemonsPdaemonStop(daemon)
        .then(() => {
          this.toastRequestSuccess();
          this.setup();
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  onClickSync() {
    this.setup();
  }

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false
  }

  onClickDeleteOk() {
    const daemon = this.$route.params.daemon;
    this.loadingDelete = true;
    this.$api2.deleteAdminDaemonsPdaemon(daemon)
        .then(() => {
          this.loadingDelete = false;
          this.showDeleteDialog = false
          this.toastRequestSuccess();
          this.moveToAdminDaemons();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
