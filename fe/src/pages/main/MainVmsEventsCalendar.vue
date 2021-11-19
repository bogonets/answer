<i18n lang="yaml">
en:
  groups: "Groups"
  events: "Events"
  calendar: "Calendar"
  first_event_day: "First Event Day"
  today: "Today"
  month: "{0} Month"
  event: "Event"
  empty: "There are no registered events."

ko:
  groups: "Groups"
  events: "Events"
  calendar: "Calendar"
  first_event_day: "처음"
  today: "오늘"
  month: "{0} 월"
  event: "이벤트"
  empty: "등록된 이벤트가 없습니다."
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
        :events="calendarEvents"
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
import {todayString, dateToString} from '@/chrono/date';

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

  loading = false;
  focusDay = todayString();

  events = [] as Array<string>;
  calendarEvents = [] as Array<any>;

  created() {
    this.updateDates();
  }

  updateDates() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2.getVmsEventsDates(group, project)
        .then(items => {
          this.loading = false;
          this.events = items;
          const focus = this.focusDay.split("-");
          const focusYear = Number.parseInt(focus[0]);
          const focusMonth = Number.parseInt(focus[1]) - 1;
          const begin = new Date(focusYear, focusMonth, 1);
          const end = new Date(focusYear, focusMonth + 1, 0);
          this.updateCalendarEvents(begin, end);
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  get focusMonth() {
    return this.focusDay.split("-")[1];
  }

  eventColor(event: any) {
    if (typeof event.color === 'undefined') {
      return '';
    } else {
      return event.color;
    }
  }

  onChangeEvents({ start, end }) {
    const min = new Date(`${start.date}T00:00:00`);
    const max = new Date(`${end.date}T23:59:59`);
    this.updateCalendarEvents(min, max);
  }

  updateCalendarEvents(begin: Date, end: Date) {
    const result = [] as Array<any>;
    const min = begin.getMilliseconds();
    const max = end.getMilliseconds();
    for (const event of this.events) {
      const eventBegin = new Date(`${event}T00:00:00`);
      const eventEnd = new Date(`${event}T23:59:59`);
      const beginMilli = eventBegin.getMilliseconds();
      if (min <= beginMilli && beginMilli <= max) {
        result.push({
          name: this.$t('event'),
          start: eventBegin,
          end: eventEnd,
          color: 'blue',
          timed: false,
        });
      }
    }
    this.calendarEvents = result;
  }

  onClickEvent({ event }) {
    console.assert(typeof event.start !== 'undefined');
    const begin = event.start as Date;
    const date = dateToString(begin);
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.moveToMainVmsEventsList(group, project, date);
  }

  onClickFirst() {
    if (this.events.length === 0) {
      this.toastWarning(this.$t('empty'));
      return;
    }
    this.focusDay = this.events[0];
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
