<template>
  <div>
    <v-menu
    v-model="openPicker"
    :close-on-content-click="false"
    offset-x offset-y
    >
      <template v-slot:activator="{ on }">
        <v-btn
        v-on="on"
        ref="button"
        :small="small"
        :text="text"
        :color="makeText()"
        >
        <span :style="`color: ${invertColor(makeText())}`">{{ makeText() }}</span>
        </v-btn>
      </template>
      <v-card>
        <v-color-picker v-model="localColor"></v-color-picker>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
  export default {
    name: "apColorPicker",
    props: {
      small: {
        type: Boolean,
        default: false
      },
      text: {
        type: Boolean,
        default: false
      },
      value: {
        default: undefined
      },
    },
    data () {
      return {
        openPicker: false,

        ////////////Input Data. (Child v-model value)///////////
        /////// { r, g, b, a } => return { r, g, b, a } ////////
        /////// #FFFFFF        => return #FFFFFF        ////////
        /////// #FFFFFFFF      => return #FFFFFFFF      ////////
        ////////////////////////////////////////////////////////
        localColor: null,
      }
    },
    watch: {
      localColor: {
        deep: true,
        immediate: true,
        handler() {
          this.$emit("input", this.localColor);
        }
      }
    },
    methods: {
      convertRGBA: function (colors) {
        if (colors) {
          if (typeof colors === "object") {
            if (colors.hasOwnProperty("r") && colors.hasOwnProperty("g") && colors.hasOwnProperty("b")) {
              return `rgba(${colors.r},${colors.g},${colors.b},${colors.a ? colors.a : 1})`
            } else if (typeof colors === "string") {
              if (colors.includes("#")) {
                var rgb = this.hexToRGB(colors);
                return rgb;
              }
            }
          }
        }
        return null;
      },
      makeText: function () {
        if (!this.localColor) {
          return "undefined";
        }
        var rgba = this.convertRGBA(this.localColor);
        if (rgba) {
          return rgba;
        } else {
          if (this.localColor) {
            return this.localColor;
          } else {
            return "undefined";
          }
        }
      },
      invertColor: function (color) {
        if (typeof color !== 'string') {
            this.$warn(this.$options.name, "invertColor", 'Not string. Input type is ', typeof color);
            return;
        }
        if (this.hexToRGB(color)) {
          color = this.hexToRGB(color);
        }
        var head = color.substring(0, 4);
        if (head === 'rgba') {
            var step1 = color.split("(");
            var step2 = step1[step1.length - 1].split(")");
            var step3 = step2[0].split(",");
            var result = head + "(";
            for (var index = 0; index < step3.length - 1; ++index) {
                var n = 255 - Number(step3[index]);
                result += n + ",";
            }
            result += Number(step3[step3.length - 1]) + ")";
            return result;
        } else if (head === 'rgb(') {
            var step1 = color.split("(");
            var step2 = step1[step1.length - 1].split(")");
            var step3 = step2[0].split(",");
            var result = head;
            for (var index = 0; index < step3.length - 1; ++index) {
                var n = 255 - Number(step3[index]);
                result += n + ",";
            }
            result += (255 - Number(step3[step3.length - 1])) + ")";
            return result;
        } else {
          return undefined;
        }
      },
      hexToRGB: function (hex, alpha) {
        if (hex) {
          if (!hex.includes("#")) {
            return null;
          }
          if (hex.length >= 9) {
            var r = parseInt(hex.slice(1, 3), 16),
            g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16),
            a = parseInt(hex.slice(7, 9), 16);
          } else {
            var r = parseInt(hex.slice(1, 3), 16),
            g = parseInt(hex.slice(3, 5), 16),
            b = parseInt(hex.slice(5, 7), 16);
          }
        }
        if (a) {
            return "rgba(" + r + ", " + g + ", " + b + ", " + a + ")";
        } else {
            return "rgb(" + r + ", " + g + ", " + b + ")";
        }
    }
    },
    created () {
      if (this.value) {
        this.localColor = this.value;
      } else {
        this.localColor = "#FFFFFFFF";
      }
    }
  }
</script>

<style scoped>

</style>
