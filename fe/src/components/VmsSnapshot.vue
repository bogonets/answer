<i18n lang="yaml">
en:
  image_failed: "Image request failed."

ko:
  image_failed: "이미지 요청에 실패했습니다."
</i18n>

<template>
  <v-row
      v-intersect="onIntersect"
      class="fill-height ma-0"
      align="center"
      justify="center"
  >
    <v-progress-circular
        v-if="loading"
        indeterminate
        color="grey lighten-5"
    ></v-progress-circular>
    <v-img
        v-else-if="existsSnapshot"
        :src="snapshotData"
        :alt="$t('image_failed')"
        :width="width"
        :height="height"
        :max-width="maxWidth"
        :max-height="maxHeight"
        :min-width="minWidth"
        :min-height="minHeight"
    ></v-img>
    <v-icon v-else>
      mdi-close
    </v-icon>
  </v-row>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class LeftTitle extends Vue {
  @Prop({type: String})
  readonly group!: string;

  @Prop({type: String})
  readonly project!: string;

  @Prop({type: Number})
  readonly eventUid!: number;

  @Prop({type: Number})
  readonly height!: number;

  @Prop({type: Number})
  readonly width!: number;

  @Prop({type: Number})
  readonly maxHeight!: number;

  @Prop({type: Number})
  readonly maxWidth!: number;

  @Prop({type: Number})
  readonly minHeight!: number;

  @Prop({type: Number})
  readonly minWidth!: number;

  @Prop({type: Boolean})
  readonly thumbnail!: boolean;

  isIntersecting = true;
  loading = false;

  snapshotContentType = '';
  snapshotEncoding = '';
  snapshotContent = '';

  get existsSnapshot() {
    const contentType = this.snapshotContentType;
    const encoding = this.snapshotEncoding;
    const content = this.snapshotContent;
    return contentType && encoding && content;
  }

  get snapshotData() {
    const contentType = this.snapshotContentType;
    const encoding = this.snapshotEncoding;
    const content = this.snapshotContent;
    return `data:${contentType};${encoding}, ${content}`;
  }

  onIntersect(entries, observer, isIntersecting) {
    this.isIntersecting = entries[0].isIntersecting;

    if (this.isIntersecting) {
      if (this.existsSnapshot) {
        return;  // Exists snapshot.
      }
      if (this.loading) {
        return;  // Load did not complete.
      }

      this.loading = true;
      const group = this.group;
      const project = this.project;
      const eventUid = this.eventUid.toString()

      let promise;
      if (this.thumbnail) {
        promise = this.$api2.getVmsEventsThumbnailsPevent(group, project, eventUid)
      } else {
        promise = this.$api2.getVmsEventsSnapshotsPevent(group, project, eventUid)
      }

      const imageTypeMsg = this.thumbnail ? 'thumbnail' : 'snapshot';
      promise
          .then(item => {
            this.loading = false;
            this.snapshotContentType = item.content_type;
            this.snapshotEncoding = item.encoding;
            this.snapshotContent = item.content;
            if (this.existsSnapshot) {
              console.debug(`Event ${eventUid} ${imageTypeMsg} load successful!`);
            } else {
              console.warn(`Event ${eventUid} ${imageTypeMsg} loaded. but content is none.`);
            }
          })
          .catch(error => {
            this.loading = false;
            this.snapshotContentType = '';
            this.snapshotEncoding = '';
            this.snapshotContent = '';
            console.error(error);
          });
    }
  }
}
</script>
