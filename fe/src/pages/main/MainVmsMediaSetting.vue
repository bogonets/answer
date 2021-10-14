<i18n lang="yaml">
en:
  groups: "Groups"
  vms: "VMS"
  setting: "Setting"
  tab:
    source: "Source"

ko:
  groups: "Groups"
  vms: "VMS"
  setting: "Setting"
  tab:
    source: "Source"
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
      <v-tab>{{ $t('tab.source') }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>

    <div v-if="isSourceTab">AA</div>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';

const TAB_INDEX_SOURCE = 0;

@Component({
  components: {
    ToolbarBreadcrumbs,
    MediaPlayer,
  }
})
export default class MainVmsMediaSetting extends VueBase {
  readonly breadcrumbs = [
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
      text: this.$t('vms'),
      disabled: false,
      href: () => this.moveToMainVmsLive(),
    },
    {
      text: this.$route.params.media,
      disabled: true,
    },
    {
      text: this.$t('setting'),
      disabled: true,
    },
  ];

  tabIndex = 0;

  get isSourceTab() {
    return this.tabIndex === TAB_INDEX_SOURCE;
  }
}
</script>
