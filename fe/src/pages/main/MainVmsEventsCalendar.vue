<i18n lang="yaml">
en:
  events: "Events"
  calendar: "Calendar"
  today: "Today"

ko:
  events: "Events"
  calendar: "Calendar"
  today: "오늘"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-toolbar flat>
      <v-btn
          outlined
          rounded
          class="mr-4"
          color="grey darken-2"
          @click="onClickToday"
      >
        {{ $t('today') }}
      </v-btn>

      <v-btn
          fab
          text
          small
          color="grey darken-2"
          @click="onClickPrev"
      >
        <v-icon small>
          mdi-chevron-left
        </v-icon>
      </v-btn>

      <v-btn
          fab
          text
          small
          color="grey darken-2"
          @click="onClickNext"
      >
        <v-icon small>
          mdi-chevron-right
        </v-icon>
      </v-btn>

    </v-toolbar>

    <v-calendar
    ></v-calendar>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueBase from '@/base/VueBase';

// import type {VmsDeviceA, VmsLayoutA, VmsEventA} from '@/packet/vms';
// import moment from 'moment-timezone';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class MainVmsEventsCalendar extends VueBase {
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
      text: this.$t('events'),
      disabled: true,
    },
    {
      text: this.$t('calendar'),
      disabled: true,
    },
  ];

  onClickToday() {
  }

  onClickPrev() {
  }

  onClickNext() {
  }
}
</script>
