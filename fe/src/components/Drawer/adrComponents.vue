<template>
  <v-navigation-drawer
    clipped
    fixed
    app
    stateless
    touchless
    right
    v-model="compo_show"
    class="answer-widget-list"
    :width="200"
  >
    <v-list class="pt-0" dense>
      <v-list-item>
        {{ $t("widget_list") }}
        <v-spacer></v-spacer>
        <v-btn
          small
          icon
          @click="closeList"
          style="border: 1px solid; margin: 0"
        >
          <v-icon>arrow_right_alt</v-icon>
        </v-btn>
      </v-list-item>
      <v-divider></v-divider>
      <template v-for="(item, index) in menu_list">
        <!-- <drag :transfer-data="item.name" :key="index" :image="require('../../assets/cyclops_icon.png')"> -->
        <drag :transfer-data="item.component" :key="index">
          <v-list-item>
            <v-list-item-icon>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>{{ $t(item.name) }}</v-list-item-content>
          </v-list-item>
        </drag>
      </template>
    </v-list>
    <!-- <v-footer absolute>
			<div class="closeList" @click="closeList">
				<v-layout row wrap justify-center align-center fill-height>
					<v-icon>arrow_right_alt</v-icon>
				</v-layout>
			</div>
    </v-footer>-->
  </v-navigation-drawer>
</template>

<script>
/**
 * Answer Drawer Components For Widget component list.
 * @author hadoo 2019-06-24
 */

export default {
  name: "adrComponents",
  props: {},
  data() {
    return {
      menu_list: []
    };
  },
  methods: {
    /**
     * Hide components drawer.
     * @public
     */
    closeList: function() {
      this.$store.commit("drawer/setCompoOpen", { bool: false });
    }
  },
  computed: {
    compo_show: {
      get: function() {
        return this.$store.getters["drawer/getCompoOpen"];
      },
      set: function(newValue) {
        return this.$store.commit("drawer/setCompoOpen", { bool: newValue });
      }
    }
  },
  created() {
    // Component List And Default Data Defined.
    this.menu_list = [
      {
        name: "camera_player",
        icon: "camera",
        component: { name: "acp-vod-player", component_data: null }
      },
      // { name: "data_table", icon: "list_alt", component: {name: "acp-table", component_data: null} },
      {
        name: "image_viewer",
        icon: "wallpaper",
        component: { name: "acp-image-viewer", component_data: null }
      },
      {
        name: "plugin",
        icon: "settings_input_component",
        component: { name: "acp-plugin", component_data: null }
      },
      {
        name: "jupyter.jupyter",
        icon: "fab fa-python",
        component: { name: "acp-jupyter", component_data: null }
      },
      {
        name: "storage_logger",
        icon: "fas fa-database",
        component: { name: "acp-blob-viewer", component_data: null }
      },
      {
        name: "lambda_viewer",
        icon: "fas fa-edit",
        component: { name: "acp-lambda-viewer", component_data: null }
      }

      // { name: "data-table-timer", icon: "list_alt", component: {name: "acp-table-timer", component_data: null} },
    ];
  },
  mounted() {
    // this.menu_list.push({ name: "add_panel", icon: "note", component: "add-panel" });
  }
};
</script>

<style scoped>
.closeList {
  width: 100%;
  height: 100%;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -o-user-select: none;
  user-select: none;
  cursor: pointer;
}
.closeList:hover {
  background-color: rgba(200, 200, 200, 0.5);
}
.answer-widget-list {
  z-index: 191;
}
</style>
