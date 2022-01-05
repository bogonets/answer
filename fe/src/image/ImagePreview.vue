<template>
  <!-- a block container is required -->
  <div>
    <img
        ref="image"
        :src="src"
        :alt="alt"
        :width="width"
        :height="height"
    >
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Ref, Watch} from 'vue-property-decorator';
import 'viewerjs/dist/viewer.css';
import Viewer from 'viewerjs';

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
  @Prop()
  readonly src!: string;

  @Prop()
  readonly alt!: string;

  @Prop()
  readonly width!: number;

  @Prop()
  readonly height!: number;

  @Prop({type: Object, default: defaultOptions})
  readonly options!: Viewer.Options;

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
    this.viewer = new Viewer(this.image, this.options);
  }

  show() {
    if (this.viewer) {
      this.viewer.show();
    }
  }
}
</script>
