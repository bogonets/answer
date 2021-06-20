<template>
  <div id="main" ref="main">
    <video 
    id="viewer"
    ref="viewer"
    width="1000"
    height="1000"
    :src="src"
    :controls="controls"
    :loop="loop"
    :autoplay="autoplay"
    :muted="muted"
    @click.right.stop="onRightClick"></video>
    <v-snackbar 
		v-model="alert" 
		top 
		right 
		absolute 
		multi-line 
		:timeout="5000" 
		style="opacity: .8; margin: 0; margin-right: 10px; margin-top: 10px">
    <div style="border: 1px solid blue; width:100%;">
      <v-alert style="opacity: .8; margin: 0px !important;" border="left" :value="alert" :type="alertType">
        <strong>{{ alertMsg }}</strong>
        <v-icon style="position: absolute; right: 15px;"  @click="alert = false" icon>clear</v-icon>
      </v-alert>
    </div>
    <!-- <v-divider vertical></v-divider> -->
    <!-- <v-icon  @click="alert = false" icon>clear</v-icon> -->
		</v-snackbar>
  </div>
</template>

<script>
export default {
  name: "AnswerSimpleVideoPlayer",
  props:{
    src: {
      type: String,
      default: undefined
    },
    controls: {
      type: Boolean,
      default: true
    },
    autoplay: {
      type: Boolean,
      default: true
    },
    loop: {
      type: Boolean,
      default: true
    }
  },
  components:{

  },
  data(){
    return {
      alert: false,
      alertType: "error",
      alertMsg: ""
    }
  },
  computed:{
    muted () {
      if (this.autoplay) {
        return true;
      } else {
        return false;
      }
    }
  },
  methods:{
    /**
     * Get video element.
     * @public
     */
    getVideoElement: function () {
      if (this.$refs.viewer) {
        return this.$refs.viewer;
      }
      return null;
    },

    /**
     * Show alert message.
     * @public
     * @param {string} - Alert message.
     * @param {string} - 'success' and 'error' type.
     */
    showAlert: function (msg, type) {
      this.alert = true;
      this.alertType = type || "error";
      this.alertMsg = msg;
    },

    /**
     * Prevent Right click event.
     * @public
     * @param {object} - Right click event.
     */
    onRightClick: function (event) {
      event.preventDefault();
    },

    /**
     * video created event.
     * @public
     * @param {object} - video dom 'loadedmetadata' event
     */
    onLoadedMetaData: function (e) {
      this.$emit("created", e);
    },

    /**
     * video before play event.
     * @public
     * @param {object} - video dom 'loadeddata' event.
     */
    onLoadedData: function (e) {
      this.$emit("beforeplay", e);
    },

    /**
     * video play event.
     * @public
     * @param {object} - video dom 'play' event.
     */
    onPlay: function (e) {
      this.showAlert(this.$t("video_load_success"), "success");
      this.$emit("play", e);
    },

    /**
     * video after play event.
     * @public
     * @param {object} - video dom 'playing' event.
     */
    onPlaying: function (e) {
      this.$emit("afterplay", e);
    },

    /**
     * video play error event.
     * @public
     * @param {object} - video dom 'error' event.
     */
    onError: function (e) {
      this.showAlert(this.$t("video_load_failed"), "error");
      this.$error(this.$options.name, "onError", e.target.error);
      this.$emit("error", e);
    }
  },
  created(){

  },
  mounted(){
    this.$nextTick()
    .then(() => {
      // loadedmetadata --> loadeddata --> play --> playing.
      if (this.$refs.viewer) {
        this.$refs.viewer.addEventListener("loadedmetadata", e => this.onLoadedMetaData(e));
        this.$refs.viewer.addEventListener("loadeddata", e => this.onLoadedData(e));
        this.$refs.viewer.addEventListener("play",       e => this.onPlay(e));
        this.$refs.viewer.addEventListener("playing",    e => this.onPlaying(e));
        this.$refs.viewer.addEventListener("error",      e => this.onError(e));
      }
    })
  },
  beforeDestroy(){
    this.$refs.viewer.removeEventListener("loadedmetadata", e => this.onLoadedMetaData(e));
    this.$refs.viewer.removeEventListener("loadeddata", e => this.onLoadedData(e));
    this.$refs.viewer.removeEventListener("play",       e => this.onPlay(e));
    this.$refs.viewer.removeEventListener("playing",    e => this.onPlaying(e));
    this.$refs.viewer.removeEventListener("error",      e => this.onError(e));
  }
}
</script>

<style scoped>
#main {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: auto;
}
#viewer {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: fill;
}
</style>
