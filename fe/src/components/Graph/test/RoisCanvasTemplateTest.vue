<template>
  <v-card class="roisWidgetCard">
    <div class="bodyZone">
      <slot name="body"></slot>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "RoisCanvasTemplateTest",
  props: {},
  components: {},
  data() {
    return {};
  },
  computed: {},
  methods: {},
  created() {},
  mounted() {}
};
</script>

<style scoped>
.roisWidgetCard {
  width: 100%;
  height: 100%;
}
.bodyZone {
  width: 100%;
  height: 100%;
}
</style>
