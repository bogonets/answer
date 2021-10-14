<i18n lang="yaml">
en:
  devices: "VMS Devices"
  edit: "Edit"
  tab:
    info: "Information"
    record: "Record"
    event: "Event"

ko:
  devices: "VMS Devices"
  edit: "Edit"
  tab:
    info: "정보"
    record: "녹화"
    event: "이벤트"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row>
      <v-col
          class="my-4"
          cols="12"
          offset-sm="1"
          sm="10"
          offset-md="2"
          md="8"
          offset-lg="3"
          lg="6"
          offset-xl="4"
          xl="4"
      >
        <v-responsive :aspect-ratio="1">
          <media-player
              hover-system-bar
          ></media-player>
        </v-responsive>
      </v-col>
    </v-row>

    <v-tabs v-model="tabIndex">
      <v-tab>{{ $t('tab.info') }}</v-tab>
      <v-tab v-show="false">{{ $t('tab.record') }}</v-tab>
      <v-tab>{{ $t('tab.event') }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>

    <v-tabs-items v-model="tabIndex">
      <v-tab-item>
        1
      </v-tab-item>
      <v-tab-item>
        2
      </v-tab-item>
      <v-tab-item>
        3
      </v-tab-item>
    </v-tabs-items>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component({
  components: {
    ToolbarBreadcrumbs,
    MediaPlayer,
  }
})
export default class AdminVmsDevicesEdit extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly breadcrumbs = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: this.$t('devices'),
      disabled: false,
      href: () => this.moveToAdminVmsDevices(),
    },
    {
      text: this.$t('edit'),
      disabled: true,
    },
    {
      text: this.$route.params.device,
      disabled: true,
    },
  ];

  tabIndex = 0;
}
</script>
