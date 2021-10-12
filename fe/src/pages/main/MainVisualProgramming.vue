<i18n lang="yaml">
en:
  vp: "VP"

ko:
  vp: "VP"
</i18n>

<template>
  <view-port>
    <v-splitpanes
        class="default-theme"
        style="position: absolute; padding: 10px;"
        @resized="refresh"
    >
      <v-pane
          :size="75"
          :min-size="25"
          style="background-color: transparent;"
      >
        <div style="width: 100%; height: 100%;">
          <visual-graph
              ref="graph"
              @openDeleteCheck="openDeleteCheck"
              @selectedLambda="selectedLambda($event)"
              @deselectedLambda="deselectedLambda($event)"
              @selectedTask="selectedTask($event)"
              @deselectedTask="deselectedTask($event)"
          >
          </visual-graph>
        </div>
      </v-pane>
      <v-pane :size="20" style="background-color: transparent;" :min-size="10">
        <div style="width: 100%; height: 100%;">
          <detail-setting
              ref="detail_setting"
              @saveSetting="saveSetting($event)"
              @deleteLambdaNTask="deleteLambdaNTask($event)"
              @onSaveTask="onSaveTask($event)"
          >
          </detail-setting>
        </div>
      </v-pane>
    </v-splitpanes>
  </view-port>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';

import '@/components/VisualGraph/litegraph.css';
import VisualGraph from '@/components/VisualGraph/vgCanvas.vue';
import DetailSetting from '@/components/VisualGraph/vgDetailSetting.vue';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    BreadcrumbMain,
    VisualGraph,
    DetailSetting,
    ViewPort,
  }
})
export default class MainVisualProgramming extends VueBase {
  refresh() {
  }

  onSaveTask(taskId) {
    this.$refs.graph['onSaveTask'](taskId);
  }

  openDeleteCheck() {
    if (this.$refs.detail_setting) {
      this.$refs.detail_setting['onDelete']();
    }
  }

  /**
   * Send lambda's data to the detail setting window when a lambda`s selected event occurs.
   * @public
   * @param {lambdaData} - Lambda`s Data.
   */
  selectedLambda(lambdaData) {
    console.log(lambdaData);
    if (this.$refs.detail_setting) {
      this.$refs.detail_setting['clearStatusTimer']();
      this.$refs.detail_setting['loadData'](lambdaData);
    } else {
      console.error(
          "[vgMain::selectedLambda] [ERROR] Ref: detail_setting is null."
      );
    }
  }

  /**
   * Initialize the detail setting window when a lambda`s deselected event occurs.
   * @public
   * @param {null}
   */
  deselectedLambda() {
    if (this.$refs.detail_setting) {
      this.$refs.detail_setting['initialize']();
    } else {
      console.error(
          "[vgMain::deselectedLambda] [ERROR] Ref: detail_setting is null."
      );
    }
  }

  /**
   * Send task's data to the detail setting window when a task`s selected event occurs.
   * @public
   * @param {taskData} - task`s Data.
   */
  selectedTask(taskData) {
    if (this.$refs.detail_setting) {
      this.$refs.detail_setting['clearStatusTimer']();
      this.$refs.detail_setting['loadData'](taskData);
    } else {
      console.error(
          "[vgMain::selectedTask] [ERROR] Ref: detail_setting is null."
      );
    }
  }

  /**
   * Initialize the detail setting window when a task`s deselected event occurs.
   * @public
   * @param {null}
   */
  deselectedTask() {
    if (this.$refs.detail_setting) {
      this.$refs.detail_setting['initialize']();
    } else {
      console.error(
          "[vgMain::deselectedTask] [ERROR] Ref: detail_setting is null."
      );
    }
  }

  /**
   * Send modified task's data to the graph canvas window when a task`s data save event occurs.
   * @public
   * @param {result} - modified lambda or task data.
   */
  saveSetting(result) {
    if (this.$refs.graph) {
      this.$refs.graph['saveSetting'](result);
    } else {
      console.error("[vgMain::saveSetting] [ERROR] Ref: graph is null.");
    }
  }

  /**
   * Send Lambda or Task delete event to graph canvas when a lambda or task delete event occurs.
   * @public
   * @param {object} - lambda or task.
   */
  deleteLambdaNTask(object) {
    if (this.$refs.graph) {
      this.$refs.graph['deleteLambdaNTask'](object);
    } else {
      console.error("[vgMain::saveSetting] [ERROR] Ref: graph is null.");
    }
  }
}
</script>

<style lang="scss" scoped>
#main {
  width: 100%;
  height: 100%;
  padding: 10px 10px 10px 10px;
  /* background-color: #fff; */
}
#visual {
  width: 80%;
  height: calc(100% - 20px);
  /* border: 1px dotted white; */
  position: absolute;
}
#mycanvas {
  /* position: absolute; */
  /* top: 48px; */
  /* height: calc(100% - 48px); */
  height: 100%;
  width: 100%;
}
#detail {
  /* border: 1px dotted white; */
  margin-left: 20px;
  width: calc(20% - 30px);
  height: calc(100% - 20px);
  position: absolute;
  left: 80%;
}
/* Transition */
.fade-enter-active {
  transition: opacity 1s;
}
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
