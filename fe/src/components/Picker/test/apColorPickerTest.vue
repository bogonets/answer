<template>
  <div style="width: 100%; height: 100%;">
    <a-color-picker v-model="color" small></a-color-picker>
  </div>
</template>

<script>
import aColorPicker from "@/components/Picker/apColorPicker.vue";
  export default {
    components: {
      aColorPicker
    },
    data () {
      return {
        color: "#FF0000"
        // color: {r: 125, g: 0, b: 0, a: 1 }
        // color: undefined
      }
    },
    watch: {
      color () {
        console.log("Color:", this.color);
      }
    },
  }
</script>

<style scoped>

</style>
