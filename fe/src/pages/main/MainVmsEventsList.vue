<i18n lang="yaml">
en:
  events: "Events"
  labels:
    device_uid: "Device UID"
    category: "Event Category"
    toady: "Today"
    search: "Search"
    description: "Description"
    new_description: "Add new description"
  period:
    date: "Date"
  category:
    all: "All"
    color: "Color"
    detection: "Detection"
    matching: "Matching"
    ocr: "OCR"
  hints:
    description: "A detailed description of the event"
  title:
    tag: "Edit Event"
  subtitle:
    tag: "View or edit specific information about an event"
  all_devices: "All Devices"
  unknown_device: "[Unknown Device]"
  no_name_device: "[No name Device]"
  empty_extra: "[Emtpy]"
  close: "Close"
  cancel: "Cancel"
  submit: "Submit"

ko:
  events: "Events"
  labels:
    device_uid: "장치 UID"
    category: "이벤트 종류"
    toady: "오늘"
    search: "검색"
    description: "상세 설명"
    new_description: "새로운 설명 추가"
  period:
    date: "날짜"
  category:
    all: "전체"
    color: "색상 비교"
    detection: "객체 탐지"
    matching: "영상 비교"
    ocr: "문자 인식"
  hints:
    description: "이벤트에 대한 상세한 설명입니다"
  title:
    tag: "이벤트 편집"
  subtitle:
    tag: "이벤트의 구체적인 정보를 열람하거나 편집합니다"
  all_devices: "전체 장치"
  unknown_device: "[알 수 없는 장치]"
  no_name_device: "[이름 없는 장치]"
  empty_extra: "[비어있습니다]"
  close: "닫기"
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="mt-4">
      <v-col class="pb-0" cols="12">
        <v-select
            dense
            outlined
            hide-details
            v-model="deviceUid"
            :items="eventDeviceUids"
            return-object
            :label="$t('labels.device_uid')"
        >
          <template v-slot:item="{ item }">
            {{ deviceName(item) }}
            <v-chip
                v-if="item !== anyDeviceUid"
                class="ml-2"
                small
                outlined
                color="primary"
            >
              <v-icon left>mdi-identifier</v-icon>
              {{ item }}
            </v-chip>
          </template>

          <template v-slot:selection="{ item }">
            {{ deviceName(item) }}
            <v-chip
                v-if="item !== anyDeviceUid"
                class="ml-2"
                small
                outlined
                color="primary"
            >
              <v-icon left>mdi-identifier</v-icon>
              {{ item }}
            </v-chip>
          </template>
        </v-select>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col class="pb-0" cols="12">
        <v-select
            dense
            outlined
            hide-details
            v-model="category"
            :items="categories"
            item-text="text"
            item-value="value"
            :label="$t('labels.category')"
        >
          <template v-slot:item="{ item }">
            <v-icon class="mr-2">{{ item.icon }}</v-icon>
            <span :class="subtitleClass">
              {{ item.text }}
            </span>
          </template>

          <template v-slot:selection="{ item }">
            <v-icon class="mr-2">{{ item.icon }}</v-icon>
            <span :class="subtitleClass">
              {{ item.text }}
            </span>
          </template>
        </v-select>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" sm="7">
        <div class="d-inline-flex flex-row align-center text-center">
          <v-icon v-if="$vuetify.breakpoint.mdAndUp" class="mr-2">
            mdi-calendar
          </v-icon>
          <v-menu
              offset-y
              transition="scale-transition"
              min-width="auto"
              v-model="showDateMenu"
              :nudge-right="datePickerSize"
              :close-on-content-click="false"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                  dense
                  rounded
                  outlined
                  readonly
                  hide-details
                  v-model="date"
                  :label="$t('period.date')"
                  v-bind="attrs"
                  v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
                no-title
                scrollable
                v-model="date"
                :min="begin"
                :max="end"
                :allowed-dates="allowedDates"
                @input="onInputDate"
            ></v-date-picker>
          </v-menu>

          <v-btn class="ml-2" color="secondary" outlined rounded @click="onClickToday">
            {{ $t('labels.toady') }}
          </v-btn>
        </div>
      </v-col>

      <v-col class="d-flex flex-row align-center" cols="12" sm="5">
        <v-spacer></v-spacer>
        <v-btn color="primary" rounded @click="onClickSearch">
          {{ $t('labels.search') }}
        </v-btn>
      </v-col>
    </v-row>

    <v-divider class="mt-4"></v-divider>
    <div ref="events-scroll-placeholder"></div>

    <v-virtual-scroll
        v-resize="onResize"
        :bench="benched"
        :items="events"
        :height="eventsHeight"
        :item-height="itemHeight"
    >
      <template v-slot:default="{ item }">
        <v-list-item :key="item.event_uid">
          <v-list-item-action>
            <v-btn fab small depressed color="primary">
              <v-icon>{{ eventCategoryIcon(item) }}</v-icon>
            </v-btn>
          </v-list-item-action>

          <div class="event-title">
            <div>
              <span :class="subtitleClass">
                {{ deviceName(item.device_uid) }}
              </span>
              <v-chip class="ml-2" small outlined color="primary">
                <v-icon left>mdi-identifier</v-icon>
                {{ item.device_uid }}
              </v-chip>
            </div>
            <div>
              <span :class="subtitleClass">
                {{ eventDateTime(item) }}
              </span>
            </div>
          </div>

          <div class="event-description">
            <span class="text-truncate text--secondary text-body-2 text-no-wrap mb-1">
              {{ extraStringify(item) }}
            </span>

            <v-btn
                v-if="!existsDescription(item)"
                color="secondary"
                rounded
                outlined
                depressed
                small
                @click="onClickTag(item)"
            >
              {{ $t('labels.new_description') }}
            </v-btn>
            <div v-else class="text--secondary ma-0">
              {{ item.description }}
              <v-btn icon small @click="onClickTag(item)">
                <v-icon small>mdi-pencil</v-icon>
              </v-btn>
            </div>
          </div>

          <div class="event-reference">
            <vms-snapshot
                thumbnail
                v-ripple
                :group="$route.params.group"
                :project="$route.params.project"
                :file="item.file"
                :width="imageWidth"
                :height="imageHeight"
            ></vms-snapshot>
          </div>
        </v-list-item>
        <v-divider></v-divider>
      </template>
    </v-virtual-scroll>

    <!-- TAG Dialog -->
    <v-dialog
        v-model="showTagDialog"
        persistent
        no-click-animation
        :max-width="widthDialog"
        @keydown.esc.stop="onClickTagCancel"
    >
      <v-card>
        <v-card-title class="mb-1">{{ $t('title.tag') }}</v-card-title>
        <v-card-subtitle>{{ $t('subtitle.tag') }}</v-card-subtitle>
        <v-divider></v-divider>
        <v-container>
          <v-textarea
              dense
              outlined
              persistent-hint
              :value="currentDescription"
              @input="onInputDescription"
              :label="$t('labels.description')"
              :hint="$t('hints.description')"
          ></v-textarea>
        </v-container>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="second" class="mr-1" @click="onClickTagCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
              :disabled="!modified"
              :loading="submitTagLoading"
              color="primary"
              @click="onClickTagSubmit"
          >
            {{ $t('submit') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <div v-show="false"></div>
  </v-container>
</template>

<script lang="ts">
import {Component, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VmsSnapshot from '@/components/VmsSnapshot.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';
import type {
  VmsDeviceA,
  VmsFilterEventQ,
  VmsEventA,
  VmsCreateEventTagQ,
  VmsUpdateEventTagQ,
} from '@/packet/vms';
import {
  EVENT_CATEGORY_ID_COLOR,
  EVENT_CATEGORY_ID_DETECTION,
  EVENT_CATEGORY_ID_MATCHING,
  EVENT_CATEGORY_ID_OCR,
  EVENT_CATEGORY_NAME_COLOR,
  EVENT_CATEGORY_NAME_DETECTION,
  EVENT_CATEGORY_NAME_MATCHING,
  EVENT_CATEGORY_NAME_OCR,
} from '@/packet/vms';
import {todayString} from '@/chrono/date';
import {iso8601ToLocal} from '@/chrono/iso8601';

const ANY_DEVICE_UID = -1;
const CONTAINER_BOTTOM_MARGIN = 12;

interface Snapshot {
  contentType: string;
  encoding: string;
  content: string;
}

@Component({
  components: {
    ToolbarBreadcrumbs,
    VmsSnapshot,
  }
})
export default class MainVmsEventsList extends VueBase {
  readonly anyDeviceUid = ANY_DEVICE_UID;
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  readonly benched = 1;
  readonly itemHeight = 64 + 4 + 4; // content height + margin top + margin bottom;

  readonly imageWidth = 64;
  readonly imageHeight = 64;

  readonly breadcrumbs = [
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
  ];

  readonly categories = [
    {
      icon: 'mdi-check-all',
      text: this.$t('category.all'),
      value: '',
    },
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
      text: this.$t('category.ocr'), value: EVENT_CATEGORY_NAME_OCR,
    },
  ];

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  @Prop({type: Number, default: 480})
  readonly widthDialog!: number;

  @Ref('events-scroll-placeholder')
  readonly eventsScrollPlaceholder!: HTMLDivElement;

  eventsHeight = 100;

  loading = false;

  deviceUid = ANY_DEVICE_UID;
  devices = [] as Array<VmsDeviceA>;

  eventDeviceUids = [] as Array<number>;
  eventDates = [] as Array<string>;

  begin = '';
  end = '';
  date = '';

  category = '';

  showDateMenu = false;

  search = false;
  events = [] as Array<VmsEventA>;

  currentEvent?: VmsEventA;

  showTagDialog = false;
  originalDescription = '';
  currentDescription = '';
  modified = false;
  submitTagLoading = false;

  created() {
    if (typeof this.$route.params.date !== 'undefined') {
      this.date = this.$route.params.date;
    } else {
      this.date = todayString();
    }
    console.debug(typeof this.date);
    console.debug(this.date);

    this.setup();
  }

  setup() {
    this.loading = true;
    (async () => {
      await this.requestSetup();
    })();
  }

  async requestSetup() {
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;

      this.devices = await this.$api2.getVmsDevices(group, project);
      const uids = await this.$api2.getVmsEventsDevices(group, project);
      this.eventDeviceUids = [ANY_DEVICE_UID, ...uids];
      this.eventDates = await this.$api2.getVmsEventsDates(group, project);
      if (this.eventDates) {
        this.begin = this.eventDates[0];
        this.end = this.eventDates[this.eventDates.length - 1];
      } else {
        this.begin = '';
        this.end = '';
      }
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  deviceName(value: number) {
    if (value === ANY_DEVICE_UID) {
      return this.$t('all_devices').toString();
    }

    const findDevice = this.devices.find(i => i.device_uid == value);
    if (typeof findDevice === 'undefined') {
      return this.$t('unknown_device').toString();
    }

    if (findDevice.name) {
      return findDevice.name;
    } else {
      return this.$t('no_name_device').toString();
    }
  }

  allowedDates(value: string) {
    return this.eventDates.includes(value);
  }

  eventCategoryIcon(item: VmsEventA) {
    switch (item.category_id) {
      case EVENT_CATEGORY_ID_COLOR:
        return 'mdi-palette';
      case EVENT_CATEGORY_ID_DETECTION:
        return 'mdi-image-search';
      case EVENT_CATEGORY_ID_MATCHING:
        return 'mdi-compare';
      case EVENT_CATEGORY_ID_OCR:
        return 'mdi-ocr';
      default:
        return 'mdi-help';
    }
  }

  eventDateTime(item: VmsEventA) {
    return iso8601ToLocal(item.time);
  }

  extraStringify(item: VmsEventA) {
    if (!item.extra) {
      return this.$t('empty_extra').toString();
    }
    return item.extra.message;
  }

  existsDescription(item: VmsEventA) {
    if (item.description === null) {
      return false;
    }
    return typeof item.description !== 'undefined';
  }

  onInputDate() {
    this.showDateMenu = true;
  }

  onClickToday() {
    this.date = todayString();
  }

  onClickSearch() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device_uid = this.deviceUid !== ANY_DEVICE_UID ? this.deviceUid : undefined;
    const category = this.category ? this.category : undefined;
    const body = {
      date: this.date,
      device_uid: device_uid,
      category: category,
    } as VmsFilterEventQ;
    this.search = true;
    this.$api2.postVmsEventsFilter(group, project, body)
        .then(items => {
          this.search = false;
          this.events = items;
          console.dir(this.events);

        })
        .catch(error => {
          this.search = false;
          this.toastRequestFailure(error);
        });
  }

  onClickTag(item: VmsEventA) {
    this.showTagDialog = true;
    this.currentEvent = item;
    this.currentDescription = item.description || '';
    this.originalDescription = item.description || '';
    this.modified = false;
  }

  onInputDescription(event: string) {
    this.currentDescription = event;
    return this.modified = this.currentDescription !== this.originalDescription;
  }

  onClickTagCancel() {
    this.currentDescription = this.originalDescription;
    this.modified = false;
    this.showTagDialog = false;
  }

  requestCreateTag(event_uid: number) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {
      event_uid: event_uid,
      description: this.currentDescription,
    } as VmsCreateEventTagQ;

    console.log('requestCreateTag');
    console.dir(body);

    this.submitTagLoading = true;
    this.$api2.postVmsEventsTags(group, project, body)
        .then(() => {
          if (this.currentEvent) {
            this.currentEvent.description = this.currentDescription;
          }
          this.originalDescription = this.currentDescription;
          this.modified = false;
          this.submitTagLoading = false;
          this.showTagDialog = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.submitTagLoading = false;
          this.toastRequestFailure(error);
        });
  }

  requestUpdateTag(tag: string) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {
      description: this.currentDescription,
    } as VmsUpdateEventTagQ;

    this.submitTagLoading = true;
    this.$api2.patchVmsEventsTagsPtag(group, project, tag, body)
        .then(() => {
          if (this.currentEvent) {
            this.currentEvent.description = this.currentDescription;
          }
          this.originalDescription = this.currentDescription;
          this.modified = false;
          this.submitTagLoading = false;
          this.showTagDialog = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.submitTagLoading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickTagSubmit() {
    if (typeof this.currentEvent === 'undefined') {
      throw new Error('Selected event is undefined');
    }

    if (this.existsDescription(this.currentEvent)) {
      this.requestUpdateTag(this.currentEvent.event_uid.toString());
    } else {
      console.log(`onClickTagSubmit -> ${this.currentEvent.event_uid}`)
      this.requestCreateTag(this.currentEvent.event_uid);
    }
  }

  onResize() {
    const size = { x: window.innerWidth, y: window.innerHeight };
    const rect = this.eventsScrollPlaceholder.getBoundingClientRect();
    this.eventsHeight = Math.abs(size.y - rect.y - (CONTAINER_BOTTOM_MARGIN * 2));
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

.event-title {
  display: flex;
  flex-direction: column;
}

.event-description {
  display: flex;
  flex-direction: column;

  justify-content: space-around;
  align-items: center;
  flex: auto;

  margin-left: 8px;

  .event-description--wrapper {
    width: 100%;
  }
}

.event-reference {
  width: 64px;
  height: 64px;
  min-width: 64px;
  min-height: 64px;
  max-width: 64px;
  max-height: 64px;

  margin: 4px;

  cursor: pointer;
}

$hover-transparent: 0.2;

.theme--light.v-application {
  .event-reference {
    background: rgba(map-get($shades, 'black'), $hover-transparent);
  }
}

.theme--dark.v-application {
  .event-reference {
    background: rgba(map-get($shades, 'white'), $hover-transparent);
  }
}
</style>
