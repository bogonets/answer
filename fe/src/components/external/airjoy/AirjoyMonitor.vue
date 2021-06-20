<template>
  <div class="main">
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12" xs="12">
        <line-graph :graphHeight="graphHeight" />
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12" xs="12">
        <line-graph :graphHeight="graphHeight" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12" xs="12">
        <line-graph :graphHeight="graphHeight" />
      </v-col>
      <v-col cols="12" xl="6" lg="6" md="12" sm="12" xs="12">
        <line-graph :graphHeight="graphHeight" />
      </v-col>
    </v-row>
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
export default class AirJoyMonitor extends Vue {
  graphHeight = "30vh";
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
  padding: 10px 10px 10px 10px;
  margin-bottom: 10px;
}
.container {
  height: 100%;
  padding: 10px 10px 0px 10px;
}
.col-height {
  height: 50%;
}
$grid-breakpoints: (
  "xs": 0,
  "sm": 340px,
  "md": 540px,
  "lg": 800px - 24px,
  "xl": 1280px - 24px,
);
</style>
