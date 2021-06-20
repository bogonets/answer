<template>
  <div id="colorDiv">
    <v-layout row wrap fill-height id="layout">
      <v-flex v-if="label" xs12>
        <span>{{label}}</span>
      </v-flex>
      <v-flex xs12>
        <input type="color" id="color" ref="color" :value="color" @input="onChange"/>
      </v-flex>
    </v-layout>
  </div>
</template>
<script>
export default {
  props: {
    label: {
      type: String,
      default: null,
    },
    resultRgbformat: {
      type: Boolean,
      default: false
    },
    value: {
      type: String
    }
  },
  components:{

  },
  data(){
    return {
      color: "#F0F0F0",
      opacity: 1,
      isOpacity: false
    }
  },
  computed:{
  },
  watch: {
    opacity() {
      var colorpicker = this.$refs.color;
      colorpicker.style.opacity = this.opacity;
    }
  },
  methods:{
    onChange: function ($event) {
      this.color = $event.target.value;
      if (this.resultRgbformat) {
        var preColor = $event.target.value;
        var split = preColor.split("#");
        var hexColor = split[1];
        var red   = parseInt(hexColor.substring(0, 2), 16);
        var blue   = parseInt(hexColor.substring(2, 4), 16);
        var green   = parseInt(hexColor.substring(4, 6), 16);
        var result = "";
        if (this.isOpacity) {
          result = "rgba(" + red + "," + blue + "," + "," + green + "," + this.opacity + ")";
        } else {
          result = 'rgb(' + red + "," + blue + "," + green + ")";
        }
        this.$emit("input", result);
      } else {
        var result = $event.target.value;
        result += Math.round(this.opacity * 255).toString(16);
        this.$emit("input", result.toUpperCase());
      }
    }
  },
  created(){

  },
  mounted(){
    if (this.value) {
      if (this.value.includes("#")) {
        var split = this.value.split("#");
        var colorValue = split[1];
        if (colorValue.length === 8) {
          var realColor = colorValue.substring(0, 6);
          var opacity = colorValue.substring(6, 8);
          var parseOpacity = parseInt(opacity, 16) / 255;
          this.color = "#" + realColor;
          this.opacity = parseOpacity;
          this.isOpacity = true;
        } else {
          this.color = this.value;
          this.opacity = 1;
          this.isOpacity = false;
        }
      }
    } else {
      this.color = "#FFFFFF";
      this.opacity = 1;
      this.isOpacity = false;
    }
  }
}
</script>
<style scoped>
#colorDiv {
  width: 100%;
  height: 100%;
}
#layout {
  margin: 0;
  padding: 0;
}
#color {
  width: 100%;
  height: 100%;
}
</style>