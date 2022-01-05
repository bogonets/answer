<template>
  <div>
    <div
        v-if="loading"
        class="d-flex flex-row align-center justify-center"
        :style="progressStyle"
    >
      <v-progress-circular
          indeterminate
          :color="progressCircularColor"
      ></v-progress-circular>
    </div>
    <!-- a block container is required -->
    <div v-else>
      <img
          ref="image"
          :src="src"
          :alt="alt"
          :width="width"
          :height="height"
          :style="imgStyle"
      />
    </div>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Ref, Watch} from 'vue-property-decorator';
import colors from 'vuetify/lib/util/colors'
import Viewer from 'viewerjs';
import 'viewerjs/dist/viewer.css';

function defaultOptions() {
  return {
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
    } as Viewer.ToolbarOptions,
  } as Viewer.Options;
}

@Component
export default class ImagePreview extends Vue {
  @Prop({type: String})
  readonly src!: string;

  @Prop({type: String})
  readonly alt!: string;

  @Prop({type: String})
  readonly backgroundColor!: string;

  @Prop({type: String})
  readonly progressColor!: string;

  @Prop({type: [String, Number]})
  readonly width!: string | number;

  @Prop({type: [String, Number]})
  readonly height!: string | number;

  @Prop({type: [String, Number]})
  readonly minWidth!: string | number;

  @Prop({type: [String, Number]})
  readonly minHeight!: string | number;

  @Prop({type: [String, Number]})
  readonly maxWidth!: string | number;

  @Prop({type: [String, Number]})
  readonly maxHeight!: string | number;

  @Prop({type: Object, default: defaultOptions})
  readonly options!: Viewer.Options;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly preview!: boolean;

  @Ref()
  readonly image!: HTMLImageElement;

  viewer?: Viewer;

  mounted() {
    this.refreshViewer();
  }

  @Watch('options')
  watchOptions() {
    this.refreshViewer();
  }

  refreshViewer() {
    if (this.preview) {
      this.viewer = new Viewer(this.image, this.options);
    }
  }

  show() {
    if (this.viewer) {
      this.viewer.show();
    }
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

  get previewBackgroundColor() {
    if (this.backgroundColor) {
      return this.backgroundColor;
    }
    if (this.$vuetify.theme.dark) {
      return colors.grey.darken3;
    } else {
      return colors.grey.lighten2;
    }
  }

  get progressStyle() {
    return {
      'width': this.width,
      'height': this.height,
      'min-width': this.minWidth,
      'min-height': this.minHeight,
      'max-width': this.maxWidth,
      'max-height': this.maxHeight,
      'background-color': this.previewBackgroundColor,
    };
  }

  get imgStyle() {
    return {
      'min-width': this.minWidth,
      'min-height': this.minHeight,
      'max-width': this.maxWidth,
      'max-height': this.maxHeight,
    };
  }
}
</script>
