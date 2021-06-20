<template>
  <v-layout row wrap>
    <v-flex xs12 v-for="(prc, index) in loads" :key="index" style="padding: 5px">
      <label>{{ prc.i18n ? $t(prc.name) : prc.name }}</label>
      <template v-if="prc.status === null || prc.status === undefined || prc.status === 'primary'">
        <v-progress-linear :indeterminate="true">
        </v-progress-linear>
        <v-icon size="15" color="primary" class="animate-rotate-infinity">fas fa-spinner</v-icon><span>{{ '  ' + $t("loading")}}</span>
      </template>
      <template v-else>
        <v-progress-linear :value="100" :color="prc.status === 'loading' ? 'lime' : prc.status">
        </v-progress-linear>
        <v-icon v-if="prc.status === 'error' || prc.status === 'success'" size="15" :color="prc.status">{{prc.status === "error" ? 'highlight_off' : 'check_circle_outline' }}</v-icon>
        <v-icon v-else size="15" color="lime" class="animate-rotate-infinity">fas fa-spinner</v-icon>
        <span v-html="returnMsg(prc)"></span>
        <v-icon v-if="prc.status === 'error'" @click="onRetry(prc)" class="icon" small icon size="15">loop</v-icon>
      </template>
      <v-divider v-if="index !== loads.length - 1" style="margin-top: 10px;"></v-divider>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  name: "AnswerProgress",
  version: "0.9.0",
  props:{
    /**
     * process list.
     */
    loadList: {
      type: Array
    },
    /**
     * Process serialize.
     */
    serialize: {
      type: Boolean,
      default: false
    }
  },
  components:{

  },
  data(){
    return {
      loads: Array
    }
  },
  computed:{
    allComplete() {
      var result = true;
      if (!this.loads) {
        return false;
      }
      if (this.loads.length !== 0) {
        for (var i = 0; i < this.loads.length; ++i) {
          if (this.loads[i]) {
            result = (result && this.loads[i].complete);
          } else {
            continue;
          }
        }
        return result;
      } else {
        return false;
      }
    }
  },
  watch: {
    allComplete() {
      if (this.allComplete) {
        setTimeout(() => {
          this.$emit("allComplete", true);
        }, 600)
      } else {
        // this.$info(this.$options.name, "watch::allComplete", '[CHECKING...] All List`s complete is not false.');
      }
    }
  },
  methods:{
    /**
     * Initialize data.
     * @public
     */
    initialize: function () {
      this.loads = this.loadList.slice();
    },

    /**
     * Destroy data.
     * @public
     */
    destroy: function () {
      this.loads.length = 0;
    },

    /**
     * Convert message.
     * @public
     * @param {object} - process info.
     */
    returnMsg: function (ps) {
      if (ps.message) {
        return ps.message;
      }
      if (ps.status === "success") {
        return this.$t("success");
      } else {
        return this.$t("failed");
      }
    },

    /**
     * Run process.
     * @public
     * @param {number} - process index.
     */
    load: async function (index) {
      try {
        this.loads[index].complete = await this.loads[index].func();
        this.loads[index].status = "success";
      } catch (e) {
        if (e.status) {
          this.loads[index].status = "loading";
          if (e.message) {
            this.loads[index].message = e.message;
          } else {
            this.loads[index].status = "error";
          }
        } else {
          this.loads[index].status = "error";
        }
        this.loads[index].complete = false;
        if (this.loads[index].onError) {
          setTimeout(() => {
            this.loads[index].onError(e)
          }, 500);
          // this.loads[index].onError(e);
        }
      }
    },

    /**
     * All process retry.
     * @public
     */
    allRetry: async function () {
      for (var i = 0; i < this.loads.length; ++i) {
        this.loads[i].complete = false;
        this.loads[i].status = "primary";
      }
      this.play();
    },

    /**
     * One process retry.
     * @public
     * @param {object} - process data.
     */
    onRetry: async function (prc) {
      prc.complete = false;
      prc.status = "primary";
      try {
        prc.complete = await prc.func();
        prc.status = "success";
      } catch (e) {
        prc.complete = false;
        prc.status = "error";
        if (prc.onError) {
          setTimeout(() => {
            prc.onError(e);
          }, 500);
        }
      }
    },

    /**
     * Run helper.
     * @public
     */
    play: function () {
      if (this.serialize) {
        this.$nextTick(async () => {
          for (var i = 0; i < this.loads.length; ++i) {
            await this.load(i);
          }
        })
      } else {
        this.$nextTick(() => {
          for (var i = 0; i < this.loads.length; ++i) {
            this.load(i);
          }
        })
      }
    }
  },

  created(){
  },

  mounted(){
    this.initialize();
    this.play();
  },

  beforeDestroy(){
    this.destroy();
  }
}
</script>

<style scoped>
.mainPage {
  width: 100%;
  height: 100%;
}
.textZone {
  width: 100%;
  height: 100%;
  border: 1px solid greenyellow;
}
.icon {
  margin-left: 5px;
}
.icon:hover {
  color: rgb(65, 118, 246);
}
span {
  font-size: 12px;
  white-space: pre-line;
}

.animate-rotate-infinity {
  animation: rotation 3s infinite linear;
  -webkit-animation: rotation 3s infinite linear;
  -webkit-transform-origin: 0% 100% 0% 100%;
  -moz-transform-origin: 0% 100% 0% 100%;
  -ms-transform-origin: 0% 100% 0% 100%;
  -o-transform-origin: 0% 100% 0% 100%;
  transform-origin: 0% 100% 0% 100%;
}
@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(359deg);
  }
}
@-webkit-keyframes rotation {
		0% {
				-webkit-transform: rotate(0deg);
		}
		100% {
				-webkit-transform: rotate(359deg);
		}
}
</style>