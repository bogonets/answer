<template>
  <div class="main blue-box">
    <line-graph />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import LineGraph from "./LineGraph.vue";

@Component({
  components: {
    LineGraph,
  },
})
export default class AirJoyGraph extends Vue {
  breakpoint = {
    thresholds: {
      xs: 340,
      sm: 540,
      md: 800,
      lg: 1280,
    },
    scrollBarWidth: 24,
  };
}
</script>

<style lang="scss">
.main {
  height: 100%;
  padding: 10px 10px 0px 10px;
}
.container {
  height: 100%;
  padding: 10px 10px 0px 10px;
}
// .blue-box {
//   border: 1px solid blue;
// }
// .red-box {
//   border: 1px solid red;
// }
// .green-box {
//   border: 1px solid green;
// }
$grid-breakpoints: (
  "xs": 0,
  "sm": 340px,
  "md": 540px,
  "lg": 800px - 24px,
  "xl": 1280px - 24px,
);
</style>
