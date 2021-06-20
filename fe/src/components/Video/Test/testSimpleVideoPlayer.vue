<template>
  <div id="TEST">
    <simple-video-player
    ref="simpleVideo"
    :src="'https://www.w3schools.com/html/mov_bbb.mp4'"
    :controls="true"
    :autoplay="true"
    :loop="true"
    @created="onCreated"
    @beforeplay="onBefore"
    @play="onPlay"
    @afterplay="onAfter"
    @error="onError"></simple-video-player>
  </div>
</template>

<script>
import SimpleVideoPlayer from "@/components/Video/SimpleVideoPlayer.vue";
export default {
  props:{

  },
  components:{
    SimpleVideoPlayer
  },
  data(){
    return {

    }
  },
  computed:{

  },
  methods:{
    onCreated: function (event) {
      console.log("Created", event);
    },
    onBefore: function (event) {
      console.log("Before", event);
    },
    onPlay: function (event) {
      console.log("Play", event);
    },
    onAfter: function (event) {
      console.log("After", event);
    },
    onError: function (event) {
      console.log("Error", event);
    }
  },
  created(){

  },
  mounted(){
    this.$nextTick()
    .then(() => {
      // check video element.
      // console.log("video", this.$refs.simpleVideo);
      // console.log("video2", this.$refs.simpleVideo.getVideoElement());
    })
  }
}
</script>

<style scoped>
#TEST {
  width: 100%;
  height: 100%;
}
</style>
