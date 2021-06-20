<template>
  <v-menu
    :dark="this.$vuetify.theme.dark"
    bottom
    offset-y
    v-model="open"
    transition="scale-transition"
    class="widget-button"
  >
    <template v-slot:activator="{ on }">
      <v-icon v-on="on" :title="$t(title)">widgets</v-icon>
    </template>
    <v-card class="widget-list">
      <div class="menu-title">
        <strong>{{ $t(title) }}</strong>
      </div>
      <v-divider></v-divider>
      <div class="widget-list-div">
        <v-container grid-list-md fluid class="widget-container">
          <v-layout row wrap>
            <v-flex v-for="(component, index) in components" xs4 :key="index">
              <drag
                :transfer-data="component.component"
                class="text-xs-center elevation-5 widget"
              >
                <v-icon :title="$t(component.name)">{{
                  component.icon
                }}</v-icon>
              </drag>
            </v-flex>
          </v-layout>
        </v-container>
      </div>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  props: {},
  components: {},
  data() {
    return {
      open: false,
      title: "widget_list",
      components: [
        {
          name: "camera_player",
          icon: "camera",
          component: { name: "acp-vod-player", component_data: null },
        },
        {
          name: "image_viewer",
          icon: "wallpaper",
          component: { name: "acp-image-viewer2", component_data: null },
        },
        {
          name: "plugin",
          icon: "settings_input_component",
          component: { name: "acp-plugin", component_data: null },
        },
        {
          name: "jupyter.jupyter",
          icon: "fab fa-python",
          component: { name: "acp-jupyter", component_data: null },
        },
      ],
    };
  },
  computed: {},
  methods: {},
  created() {},
  mounted() {},
};
</script>

<style scoped>
.widget-button {
  z-index: 10000;
}
.widget-list {
  background-color: rgb(50, 50, 105);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 0px 20px 15px 20px;
}
.widget-list-div {
  width: 250px;
}
.widget-container {
  padding: 15px;
}
.widget {
  padding: 0;
  padding-top: 2px;
  margin: 0;
  border: 1px solid rgba(200, 200, 200, 0.6);
  border-radius: 15px;
}
.menu-title {
  height: 40px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
}
</style>
