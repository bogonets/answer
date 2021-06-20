<template>
  <div class="timer-div">
  </div>
</template>
<script>
import { clearInterval, setInterval } from 'timers';
export default {
  name: "answerTimer",
  props:{
    timer: {
      type: Boolean,
      default: false,
    },
    function: {
      type: Function,
      default: null
    },
    interval: {
      type: Number,
      default: 5
    }
  },
  components:{

  },
  data(){
    return {
      loop: null,      
    }
  },
  computed:{

  },
  watch: {
    timer () {
      this.watchStatus(this.timer);
    },
    interval () {
      this.watchStatus(this.timer);
    }
  },
  methods:{
    loopFunciton: function ()  {
      this.function;
      // this.$emit("onTimer", true);
    },
    onStart: function () {
      if (this.loop == null) {
        this.loop = setInterval(this.function, this.interval * 1000);
      }
    },
    onClose: function () {
      if (this.loop != null) {
        clearInterval(this.loop);
        this.loop = null;
      }
    },
    watchStatus: function (isStart) {
      if (isStart) {
        this.onClose();
        this.onStart();
      } else {
        this.onClose();
      }
    }
  },
  created(){

  },
  mounted(){

  },
  beforeDestroy() {
    this.onClose();
  }
}
</script>
<style scoped>
.timer-div {
  z-index: -1;
  width: 0%;
  height: 0%;
}
</style>