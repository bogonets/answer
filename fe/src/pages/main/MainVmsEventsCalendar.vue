<i18n lang="yaml">
en:
  groups: "Groups"
  events: "Events"
  calendar: "Calendar"
  first_event_day: "First Event Day"
  today: "Today"
  month: "{0} Month"

ko:
  groups: "Groups"
  events: "Events"
  calendar: "Calendar"
  first_event_day: "처음"
  today: "오늘"
  month: "{0} 월"
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
          @click="onClickFirst"
      >
        {{ $t('first_event_day') }}
      </v-btn>

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

      <span class="text--primary text-h5 font-weight-bold">
        {{ $t('month', [focusMonth]) }}
      </span>

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
        ref="calendar"
        class="events-calendar"
        v-model="focusDay"
        type="month"
        color="primary"
        :weekdays="[0, 1, 2, 3, 4, 5, 6]"
        :events="events"
        event-overlap-mode="stack"
        event-overlap-threshold="30"
        :event-color="eventColor"
        @change="onChangeEvents"
        @click:event="onClickEvent"
    ></v-calendar>

  </v-container>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import {VCalendar} from 'vuetify/lib/components/VCalendar';
import {todayString} from '@/chrono/date';

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

  @Ref()
  readonly calendar!: VCalendar;

  focusDay = todayString();
  events = [] as Array<any>;

  get focusMonth() {
    return this.focusDay.split("-")[1];
  }

  eventColor(event) {
    return event.color;
  }

  onChangeEvents({ start, end }) {
    // const events = [];
    // const min = new Date(`${start.date}T00:00:00`);
    // const max = new Date(`${end.date}T23:59:59`);
    // const days = (max.getTime() - min.getTime()) / 86400000;

    const events = [
      {
        name: 'AAA',
        start: this.focusDay,
        end: this.focusDay,
        color: 'blue',
        timed: false,
      }
    ];
    this.events = events;
  }

  onClickEvent({ nativeEvent, event }) {
    console.debug(`onClickEvent: ${nativeEvent}, ${event}`)
  }

  onClickFirst() {
  }

  onClickToday() {
    this.focusDay = todayString();
  }

  onClickPrev() {
    this.calendar.prev();
  }

  onClickNext() {
    this.calendar.next();
  }
}
</script>

<style lang="scss" scoped>
.events-calendar::v-deep {
  .v-calendar-weekly__day {
    min-height: 80px;
  }
  .v-calendar-weekly__day-label {
    margin-bottom: 4px;
  }
}
</style>
