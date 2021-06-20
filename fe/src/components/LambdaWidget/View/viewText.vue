<template>
  <div class="textZone" ref="textZone">
    <pre
      v-if="!!src"
      class="text"
      ref="text"
      v-html="src"
    >
    </pre>
    <div v-else class="non-text">
      <v-container fill-height>
        <v-row no-gutters>
          <v-col cols="12" class="text-center">
            {{ $t(noTextMessage) }}
          </v-col>
        </v-row>
      </v-container>
    </div>
  </div>
</template>

<script>
export default {
  name: "viewText",
  props:{
    fontSize: {
      type: Number,
      default: 12
    }
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
      noTextMessage: "no_text"
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
      if (typeof this.src !== 'string') {
        try {
          if (typeof this.src === 'object') {
            this.src = JSON.stringify(this.src);
          } else if (typeof thi.src === 'array') {
            this.src = this.src.toString();
          } else {
            this.src = `${this.src}`;
          }
        } catch (e) {
          this.$warn(this.$options.name, "setSource", "Type error: is Not String. And Convert Failed. Source is:", this.src);
        }
      }
    }
  },
  created(){
  },
  mounted(){
    this.$nextTick()
    .then(() => {
      this.$refs.textZone.style['font-size'] = this.fontSize + 'px';
    })
  }
}
</script>

<style scoped>
.textZone {
  display: inline-block;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: auto;
}
.text {
  position: absolute;
  width: 100%;
  height: 100%;
  white-space: pre-line;
}
.non-text {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(125, 125, 125, 0.5);
}
/* .non-image-pattern {
  background:url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAJ0lEQVQoU2N0d3b/z4AGysrK0IUYGIeCwr0792J4pqurC9MzQ0AhAIQrKBVcGz7hAAAAAElFTkSuQmCC") repeat;
} */
</style>
