<template>
  <v-card style="height: 100%"
    ><v-toolbar dense height="55px">
      <slot name="topLeft"> </slot>
      <v-spacer></v-spacer>
      <slot name="topCenter"> </slot>
      <v-spacer></v-spacer>
      <slot name="topRight"> </slot>
    </v-toolbar>
    <v-container>
      <v-layout class="split" grid-list-md>
        <v-flex class="left" col-4 pa-0>
          <slot name="panel"></slot>
        </v-flex>
        <v-flex class="right" col-8 pa-0>
          <slot name="body"></slot>
        </v-flex>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
import Vue from "vue";
import Component from "vue-class-component";

@Component
export default class RoisWidgetTemplate extends Vue {}
</script>

<style scoped>
.split {
  position: absolute;
  top: 55px;
  right: 0;
  bottom: 0;
  left: 0;
  height: 100%;
}
.left {
  overflow-y: scroll;
  height: 100%;
  position: relative;
}
.right {
  height: 100%;
  position: relative;
}
</style>
