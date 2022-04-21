<i18n lang="yaml">
en:
  image_failed: 'Image request failed.'

ko:
  image_failed: '이미지 요청에 실패했습니다.'
</i18n>

<template>
  <div class="d-flex flex-row align-center justify-center" @click="onClick">
    <v-progress-circular
      v-if="loading"
      indeterminate
      :color="progressCircularColor"
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
    <v-icon v-else>mdi-close</v-icon>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';
import colors from 'vuetify/lib/util/colors';
import Viewer from 'viewerjs';
import 'viewerjs/dist/viewer.css';

function defaultOptions() {
  return {} as Viewer.Options;
}

@Component
export default class VmsSnapshot extends Vue {
  @Prop({type: String})
  readonly group!: string;

  @Prop({type: String})
  readonly project!: string;

  @Prop({type: Number})
  readonly event!: number;

  @Prop({type: String})
  readonly progressColor!: string;

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

  loading = false;
  contentType = '';
  encoding = '';
  content = '';

  mounted() {
    this.loading = true;
    const group = this.group;
    const project = this.project;
    const event = this.event;

    this.$api2
      .getVmsEventsThumbnailsPevent(group, project, event.toString())
      .then(item => {
        this.loading = false;
        this.contentType = item.content_type;
        this.encoding = item.encoding;
        this.content = item.content;
      })
      .catch(error => {
        this.loading = false;
        this.contentType = '';
        this.encoding = '';
        this.content = '';
        console.error(error);
      });
  }

  get existsSnapshot() {
    return this.contentType && this.encoding && this.content;
  }

  get snapshotData() {
    return `data:${this.contentType};${this.encoding}, ${this.content}`;
  }

  get progressCircularColor() {
    if (this.progressColor) {
      return this.progressColor;
    }
    if (this.$vuetify.theme.dark) {
      return colors.grey.darken1;
    } else {
      return colors.grey.lighten5;
    }
  }

  onClick() {
    const group = this.group;
    const project = this.project;
    const event = this.event;

    this.$api2
      .getVmsEventsSnapshotsPevent(group, project, event.toString())
      .then(item => {
        const contentType = item.content_type;
        const encoding = item.encoding;
        const content = item.content;
        const image = new Image();
        image.src = `data:${contentType};${encoding}, ${content}`;
        image.alt = event.toString();
        const viewer = new Viewer(image, {
          navbar: false,
          toolbar: {
            flipHorizontal: 1,
            flipVertical: 1,
            next: 0,
            oneToOne: 1,
            play: 0,
            prev: 0,
            reset: 1,
            rotateLeft: 1,
            rotateRight: 1,
            zoomIn: 1,
            zoomOut: 1,
          },
          hidden: function () {
            viewer.destroy();
          },
        });
        viewer.show();
      })
      .catch(error => {
        console.error(error);
      });
  }
}
</script>
