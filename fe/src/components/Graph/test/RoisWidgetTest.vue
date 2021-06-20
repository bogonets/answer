<template>
  <div style="width: 100%; height: 100%; display: inline-block">
    <window>
      <template v-slot:topLeft>
        <template v-for="(topLeft, index) in topLefts">
          <!-- prettier-ignore -->
          <component
            :key="`topleft-${index}`"
            :taskName="taskName"
            :lambdaUid="lambdaUid"
            :is="topLeft.name"
            :ref="topLeft.ref"
            @signal="onSignalData($event, topLeft.trans, topLeft.transData)"
            @transData="transData($event, topLeft.trans, topLeft.transData)"
            @writeSuccess="onWriteSuccess($event)"
            :sendData="getSendDataOfTopComponent(topLeft)"
            v-bind="topLeft.props"
            :style="topLeft.style ? topLeft.style : undefined"
          >
          </component>
        </template>
      </template>

      <template v-slot:topCenter>
        <template v-for="(topCenter, index) in topCenters">
          <!-- prettier-ignore -->
          <component
            :key="`topcenter-${index}`"
            :taskName="taskName"
            :lambdaUid="lambdaUid"
            :is="topCenter.name"
            :ref="topCenter.ref"
            @signal="onSignalData($event, topCenter.trans, topCenter.transData)"
            @transData="transData($event, topCenter.trans, topCenter.transData)"
            @writeSuccess="onWriteSuccess($event)"
            :sendData="getSendDataOfTopComponent(topCenter)"
            v-bind="topCenter.props"
            :style="topCenter.style ? topCenter.style : undefined"
          >
          </component>
        </template>
      </template>

      <template v-slot:topRight>
        <template v-for="(topRight, index) in topRights">
          <!-- prettier-ignore -->
          <component
            :key="`topright-${index}`"
            :taskName="taskName"
            :lambdaUid="lambdaUid"
            :is="topRight.name"
            :ref="topRight.ref"
            @signal="onSignalData($event, topRight.trans, topRight.transData)"
            @transData="transData($event, topRight.trans, topRight.transData)"
            @writeSuccess="onWriteSuccess($event)"
            :sendData="getSendDataOfTopComponent(topRight)"
            v-bind="topRight.props"
            :style="topRight.style ? topRight.style : undefined"
          >
          </component>
        </template>
      </template>

      <template v-slot:panel>
        <template v-for="(panel, index) in panels">
          <component
            :key="`panel-${index}`"
            :lambdaProps="lambdaProps"
            :taskName="taskName"
            :lambdaUid="lambdaUid"
            :is="panel.name"
            :ref="panel.ref"
            :roisInfos="roisInfos"
            v-bind="panel.props"
            :style="panel.style ? panel.style : undefined"
            @capture="onCapture($event)"
            @save="onSave($event)"
            @delete="onDelete($event)"
            @signal="onSignalData($event, panel.trans, panel.transData)"
            @select="onSelectProperty($event)"
            @roisinfos="setRoisInfos($event)"
          >
          </component>
        </template>
      </template>

      <template v-slot:body>
        <template v-for="(body, index) in bodys">
          <component
            :key="`body-${index}`"
            :lambdaProps="lambdaProps"
            :taskName="taskName"
            :lambdaUid="lambdaUid"
            :is="body.name"
            :ref="body.ref"
            v-bind="body.props"
            :style="body.style ? body.style : undefined"
            @rois="onDonePainting($event)"
            @clear="onDrawClear()"
          >
          </component>
        </template>
      </template>
    </window>
    <v-icon
      v-if="isDialog"
      size="20"
      class="close--icon"
      @click="$emit('close')"
      >close</v-icon
    >
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from "vue-property-decorator";

import Window from "@/components/Graph/Window/roisWidgetTemplate.vue";

// Option
import getPropertyButton from "@/components/LambdaWidget/Option/getPropertyButton.vue";
import setPropertyButton from "@/components/LambdaWidget/Option/setPropertyButton.vue";
import signalButton from "@/components/LambdaWidget/Option/signalButton.vue";
import RoisControlPanel, {
  RoisPanelEvent
} from "@/components/Graph/RoisControlPanel.vue";

// View
import viewImage from "@/components/LambdaWidget/View/viewImage.vue";
import drawCanvas from "@/components/LambdaWidget/View/drawCanvas.vue";

import * as BaseRois from "@/components/Graph/BaseRois.ts";

@Component({
  components: {
    Window,
    RoisControlPanel,
    viewImage,
    drawCanvas,
    signalButton,
    getPropertyButton,
    setPropertyButton
  }
})
export default class RoisWidget extends Vue {
  @Prop({ default: undefined }) lambdaProps;
  @Prop({ type: String, default: undefined }) taskName;
  @Prop({ type: String, default: undefined }) lambdaUid;
  @Prop({ type: Object, default: undefined }) metaData;
  @Prop({ type: Boolean, default: false }) isDialog;

  private roisInfos = new BaseRois.RoiInfoDictionary();
  private topLefts: Array<object> = new Array<object>();
  private topCenters: Array<object> = new Array<object>();
  private topRights: Array<object> = new Array<object>();
  private panels: Array<object> = new Array<object>();
  private bodys: Array<object> = new Array<object>();
  private selectedPropertyIndex = -1;

  private readonly propertyValue = undefined;
  private readonly lambdaPropertyKeyRois = "rois";
  private readonly lambdaPropertyKeyProps = "props";
  private readonly lambdaPropertyKeySnaps = "snaps";

  /** MIME: image/jpeg;base64 */
  private _cachedSignalImage = "";

  created() {
    var meta = this.metaData;
    var lambdaData = null;
    if (meta.info) {
      if (meta.info.lambdaData) {
        lambdaData = meta.info.lambdaData;
      }
    }
    if (meta.components.body) {
      this.$nextTick().then(() => {
        this.makeBody(meta.components.body, lambdaData);
      });
    }
    if (meta.components.top) {
      setTimeout(() => {
        this.makeTop(meta.components.top, lambdaData);
      }, 1000);
    }
    if (meta.components.panel) {
      this.$nextTick().then(() => {
        this.makePanel(meta.components.panel, lambdaData);
      });
    }
  }

  onCapture(event: RoisPanelEvent): void {
    if (!this._cachedSignalImage) {
      this.$warn(this.$options.name, "onCapture", "Not exists cached image!");
      return;
    }

    if (!this.roisInfos.has(event.index)) {
      this.$info(
        this.$options.name,
        "onCapture",
        `Create new property: ${event.index}`
      );
      this.roisInfos.set(event.index, new BaseRois.RoiInfo());
    }
    this.roisInfos.get(
      event.index
    ).snapshotInBase64Jpeg = this._cachedSignalImage;
  }

  onSave(event: RoisPanelEvent): void {
    if (event.data === undefined) {
      this.$error(
        this.$options.name,
        "onSave",
        `Undefined RoI property: ${event.index}`
      );
      return;
    }

    this.selectedPropertyIndex = event.index;
    if (!this.roisInfos.has(event.index)) {
      this.$info(
        this.$options.name,
        "onSave",
        `Create new property: ${event.index}`
      );
      this.roisInfos.set(event.index, new BaseRois.RoiInfo());
    }

    this.roisInfos.get(event.index).property = event.data;
  }

  onDelete(event: RoisPanelEvent): void {
    if (!this.roisInfos.has(event.index)) {
      this.$warn(
        this.$options.name,
        "onDelete",
        `Not exists property: ${event.index}`
      );
      return;
    }
    this.onDrawClear();
    this.$refs["image"][0].setSource("");
    this.$refs["canvas"][0].canvasClear(true);
    this.roisInfos.delete(event.index);

    let roisInfosCloned = new BaseRois.RoiInfoDictionary();

    let i=0;
    for(const info of this.roisInfos.values()){
      roisInfosCloned.set(i, info);
      i++;
    }
    this.roisInfos = roisInfosCloned;
  }

  /**
   * Received a 'signal' message from the c2core.
   */
  onSignalData(data, ref, des) {
    this.$refs[ref][0][des](data);
    this._cachedSignalImage = data;
  }

  requsetSetProperty(key: string, val: string): void {
    this.$api
      .setPropertyValueWithNative(
        this.$store.getters["user/getAccessToken"],
        this.$store.getters["user/getRefreshToken"],
        this.$store.getters["project/getSelectProject"],
        this.taskName,
        this.lambdaUid,
        key,
        val
      )
      .then(response => {
        this.$debug(
          this.$options.name,
          "requsetSetProperty",
          `Response result: ${response}`
        );
      })
      .catch(error => {
        this.$error(
          this.$options.name,
          "requsetSetProperty",
          `Error: ${error}`
        );
      })
      .then(() => {
        // done.
      });
  }

  /**
   * RoisControlPanel Event
   *
   */
  onSelectProperty(event) {
    if (!this.roisInfos.has(event.index)) {
      this.$warn(
        this.$options.name,
        "onSelectProperty",
        `Not exists index: ${event.index}`
      );
      this.$refs["image"][0].setSource("");
      this.$refs["canvas"][0].canvasClear(true);
      return;
    }

    this.selectedPropertyIndex = event.index;
    const selected_rois = this.roisInfos.get(event.index);

    // Draw base64 encoded image.
    this.$refs["image"][0].setSource(selected_rois.snapshotInBase64Jpeg);
    this.$refs["canvas"][0].canvasClear(true);
    this.$refs["canvas"][0].setStrokeEndStyle(
      this.roisInfos
        .get(event.index)
        .property.lineStyleColorValue.getIntegerList()
    );

    this.$refs["canvas"][0].setPolygons(
      JSON.stringify(new Array(selected_rois.getPoints()))
    );
  }

  /**
   * DrawCanvas Event
   *
   */
  onDonePainting(event) {
    this.roisInfos.get(this.selectedPropertyIndex).points = new Array<
      BaseRois.Point
    >();
    for (let i = 0; i < event[0].length; i = i + 2) {
      this.roisInfos
        .get(this.selectedPropertyIndex)
        .points.push(new BaseRois.Point(event[0][i], event[0][i + 1]));
    }
  }

  requsetGetProperty(
    key: string,
    responseCallback: (val: string) => void
  ): void {
    this.$api
      .getPropertyValueWithNative(
        this.$store.getters["user/getAccessToken"],
        this.$store.getters["user/getRefreshToken"],
        this.$store.getters["project/getSelectProject"],
        this.taskName,
        this.lambdaUid,
        key
      )
      .then(response => {
        this.$debug(
          this.$options.name,
          "requsetGetProperty",
          `Response result: ${response}`
        );
        responseCallback(response.data);
      })
      .catch(error => {
        this.$error(
          this.$options.name,
          "requsetGetProperty",
          `Error: ${error}`
        );
      })
      .then(() => {
        // done.
      });
  }

  makeTop(tops, lambdaData) {
    for (var top of tops) {
      let component = {};
      component["name"] = `${top.name}`;
      component["ref"] = `${top.ref}`;
      component["props"] = top.props;
      component["style"] = `${top.style}`;
      if (top.transData) {
        let spt = top.transData.split(".");
        component["trans"] = spt[0];
        component["transData"] = spt[1];
      }
      if (top.sendData) {
        let spt = top.sendData.split(".");
        component["send"] = spt[0];
        component["sendData"] = spt[1];
      }

      if (top.align.toLowerCase() === "left") {
        this.topLefts.push(component);
      } else if (top.align.toLowerCase() === "center") {
        this.topCenters.push(component);
      } else {
        this.topRights.push(component);
      }

      this.$nextTick().then(() => {
        if (lambdaData) {
          if (lambdaData.where === "top") {
            this.$refs[`${lambdaData.ref}`][0][lambdaData.function](
              lambdaData.params,
              this.propertyValue
            );
          }
        }
      });
      this.$debug(
        this.$options.name,
        "makeTop Result:",
        this.topLefts,
        this.topCenters,
        this.topRights
      );
    }
    this.$debug(
      this.$options.name,
      "makeTop",
      `current data in this.$refs : ${this.$refs}`
    );
  }

  makePanel(panels, lambdaData) {
    for (var panel of panels) {
      this.panels.push({
        name: `${panel.name}`,
        ref: `${panel.ref}`,
        props: panel.props,
        style: `${panel.style}`
      });
    }
    this.$nextTick().then(() => {
      if (lambdaData) {
        if (lambdaData.where === "panel") {
          this.$refs[`${lambdaData.ref}`][0][lambdaData.function](
            lambdaData.params,
            this.propertyValue
          );
        }
      }
    });
  }

  makeBody(bodys, lambdaData) {
    for (var body of bodys) {
      var component = {};
      component["name"] = `${body.name}`;
      component["ref"] = `${body.ref}`;
      component["props"] = body.props;
      component["style"] = `${body.style}`;
      this.bodys.push(component);
    }

    this.$nextTick().then(() => {
      if (lambdaData) {
        if (lambdaData.where === "body") {
          this.$refs[`${lambdaData.ref}`][0][lambdaData.function](
            lambdaData.params,
            this.propertyValue
          );
        }
      }
    });
  }

  transData(data, ref, des) {
    this.$refs[ref][0][des](data);
  }

  getSendData(ref, des) {
    try {
      return this.$refs[ref][0][des]();
    } catch {
      return ref; // In this case, it is a contant data.
    }
  }

  setRoisInfos(event) {
    this.roisInfos = event;
  }

  onWriteSuccess(data) {
    this.$emit("writeSuccess", data);
  }

  onDrawClear() {
    if (this.$refs["panel"][0].currentListIndex) {
      this.roisInfos.get(
        this.$refs["panel"][0].currentListIndex
      ).points = new Array<BaseRois.Point>();
    }
  }

  getSendDataOfTopComponent(component) {
    console.assert(
      component !== undefined,
      "The 'component' argument is undefined in the getSendDataOfTopComponent() method."
    );
    return component.sendData
      ? this.$refs[component.send][0][component.sendData]()
      : undefined;
  }
}
</script>

<style scoped>
.absolute {
  position: absolute;
}
.close--icon {
  position: absolute;
  top: -10px;
  right: -10px;
  border: 1px solid;
  border-radius: 15px;
}
</style>
