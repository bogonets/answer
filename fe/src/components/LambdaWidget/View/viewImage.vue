<template>
  <div class="imageZone">
    <img
      v-if="!!src"
      class="image"
      ref="image"
      :alt="$t('no_img')"
      :src="src"
      @load="onImageLoad($event)"
      @error="onImageError($event)"
    />
    <div v-else class="non-image">
      <v-container fill-height>
        <v-row no-gutters>
          <v-col cols="12" class="text-center">
            {{ $t(noImageMessage) }}
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
export default {
  name: "viewImage",
  props:{
    // src: {
    //   type: String,
    //   default: undefined
    // }
  },
  components:{

  },
  data(){
    return {
      src: undefined,
      noImageMessage: "no_img"
    }
  },
  computed:{
    originSize () {
      if (this.$refs.image) {
        return [0, 0];
      } else {
        return [0, 0];
      }
    }
  },
  methods:{
    setSource: function (data) {
      this.$debug(this.$options.name, "setSource", "Data:", data);
      this.src = data;  
    },
    getSource: function(){
      this.$debug(this.$options.name, "getSource", "Src:", this.src);
      this.$emit("getSource",this.src);
    },
    onImageLoad: function ($event) {
      /** Empty */
    },
    onImageError: function ($event) {
      this.$error(this.$options.name, "onImageLoadError", "Image load failed. Source:", this.src);
      this.src = undefined;
      this.noImageMessage = "image_load_failed";
    }
  },
  created(){
  },
  mounted(){
  }
}
</script>

<style scoped>
.imageZone {
  display: inline-block;
  position: absolute;
  width: 100%;
  height: 100%;
}
.image {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: fill;
}
.non-image {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(125, 125, 125, 0.5);
}
/* .non-image-pattern {
  background:url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAJ0lEQVQoU2N0d3b/z4AGysrK0IUYGIeCwr0792J4pqurC9MzQ0AhAIQrKBVcGz7hAAAAAElFTkSuQmCC") repeat;
} */
</style>
