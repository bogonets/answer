<template>
  <div style="width: 100%; height: 100%; display: inline-block">
    <window>
      <template v-slot:topLeft>
        <template v-for="(topLeft, index) in topLefts">
          <component
          :key="`topleft-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="topLeft.name"
          :ref="topLeft.ref"
          @signal="signalData($event, topLeft.trans, topLeft.transData)"
          @transData="transData($event, topLeft.trans, topLeft.transData)"
          @writeSuccess="writeSuccess($event)"
          :sendData="topLeft.sendData ? $refs[topLeft.send][0][topLeft.sendData]() : undefined"
          v-bind="topLeft.props"
          :style="topLeft.style ? topLeft.style : undefined">
          </component>
        </template>
      </template>
      <template v-slot:topCenter>
        <template v-for="(topCenter, index) in topCenters">
          <component
          :key="`topcenter-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="topCenter.name"
          :ref="topCenter.ref"
          @signal="signalData($event, topCenter.trans, topCenter.transData)"
          @transData="transData($event, topCenter.trans, topCenter.transData)"
          @writeSuccess="writeSuccess($event)"
          :sendData="topCenter.sendData ? $refs[topCenter.send][0][topCenter.sendData]() : undefined"
          v-bind="topCenter.props"
          :style="topCenter.style ? topCenter.style : undefined">
          </component>
        </template>
      </template>
      <template v-slot:topRight>
        <template v-for="(topRight, index) in topRights">
          <component
          :key="`topright-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="topRight.name"
          :ref="topRight.ref"
          @signal="signalData($event, topRight.trans, topRight.transData)"
          @transData="transData($event, topRight.trans, topRight.transData)"
          @writeSuccess="writeSuccess($event)"
          :sendData="topRight.sendData ? $refs[topRight.send][0][topRight.sendData]() : undefined"
          v-bind="topRight.props"
          :style="topRight.style ? topRight.style : undefined">
          </component>
        </template>
      </template>
      <template v-slot:body>
        <template v-for="(body, index) in bodys">
          <component
          :key="`body-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="body.name"
          :ref="body.ref"
          v-bind="body.props"
          :style="body.style ? body.style : undefined">
          </component>
        </template>
      </template>
      <template v-slot:footerLeft>
        <template v-for="(footerLeft, index) in footerLefts">
          <component
          :key="`footerleft-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="footerLeft.name"
          :ref="footerLeft.ref"
          @signal="signalData($event, footerLeft.trans, footerLeft.transData)"
          @transData="transData($event, footerLeft.trans, footerLeft.transData)"
          @writeSuccess="writeSuccess($event)"
          :sendData="footerLeft.sendData ? $refs[footerLeft.send][0][footerLeft.sendData]() : undefined"
          v-bind="footerLeft.props"
          :style="footerLeft.style ? footerLeft.style : undefined">
          </component>
        </template>
      </template>
      <template v-slot:footerCenter>
        <template v-for="(footerCenter, index) in footerCenters">
          <component
          :key="`footercenter-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="footerCenter.name"
          :ref="footerCenter.ref"
          @signal="signalData($event, footerCenter.trans, footerCenter.transData)"
          @transData="transData($event, footerCenter.trans, footerCenter.transData)"
          @writeSuccess="writeSuccess($event)"
          :sendData="footerCenter.sendData ? $refs[footerCenter.send][0][footerCenter.sendData]() : undefined"
          v-bind="footerCenter.props"
          :style="footerCenter.style ? footerCenter.style : undefined">
          </component>
        </template>
      </template>
      <template v-slot:footerRight>
        <template v-for="(footerRight, index) in footerRights">
          <component
          :key="`footerright-${index}`"
          :taskName="taskName"
          :lambdaUid="lambdaUid"
          :is="footerRight.name"
          :ref="footerRight.ref"
          @signal="signalData($event, footerRight.trans, footerRight.transData)"
          @transData="transData($event, footerRight.trans, footerRight.transData)"
          @writeSuccess="writeSuccess($event)"
          :sendData="footerRight.sendData ? $refs[footerRight.send][0][footerRight.sendData]() : undefined"
          v-bind="footerRight.props"
          :style="footerRight.style ? footerRight.style : undefined">
          </component>
        </template>
      </template>
    </window>
    <v-icon v-if="isDialog" size="20" class="close--icon" @click="$emit('close')">close</v-icon>
  </div>
</template>

<script>
import Window from "@/components/LambdaWidget/Window/lambdaWidgetTemplate.vue";
// Option
import getPropertyButton from "@/components/LambdaWidget/Option/getPropertyButton.vue";
import setPropertyButton from "@/components/LambdaWidget/Option/setPropertyButton.vue";
import signalButton from "@/components/LambdaWidget/Option/signalButton.vue";

// View
import viewText from "@/components/LambdaWidget/View/viewText.vue";
import viewImage from "@/components/LambdaWidget/View/viewImage.vue";
import drawCanvas from "@/components/LambdaWidget/View/drawCanvas.vue";

export default {
  name: "LambdaWidget",
  props: {
    taskName: {
      type: String,
      default: undefined
    },
    lambdaUid: {
      type: String,
      default: undefined
    },
    metaData: {
      type: Object,
      default: undefined
    },
    isDialog: {
      type: Boolean,
      default: false
    }
  },
  components: {
    Window,
    getPropertyButton,
    setPropertyButton,
    viewText,
    viewImage,
    drawCanvas,
    signalButton
  },
  data() {
    return {
      topLefts: [],
      topCenters: [],
      topRights: [],
      bodys: [],
      footerLefts: [],
      footerCenters: [],
      footerRights: [],
    };
  },
  computed: {},
  methods: {
    makeTop: function (tops, lambdaData) {
      for (var top of tops) {
        var component = {};
        component.name = `${top.name}`;
        component.ref = `${top.ref}`; 
        component.props = top.props;
        component.style = `${top.style}`;
        if (top.transData) {
          var spt = top.transData.split(".");
          component.trans = spt[0];
          component.transData = spt[1];
        }
        if (top.sendData) {
          var spt = top.sendData.split(".");
          component.send = spt[0];
          component.sendData = spt[1];
        }
        if (top.align.toLowerCase() === "left") {
          this.topLefts.push(component);
        } else if (top.align.toLowerCase() === "center") {
          this.topCenters.push(component);
        } else {
          this.topRights.push(component);
        }
        this.$nextTick()
        .then(() => {
          if (lambdaData) {
            if (lambdaData.where === "top") {
              this.$refs[`${lambdaData.ref}`][0][lambdaData.function](lambdaData.params, this.propertyValue);
            }
          }
        })
        this.$debug(this.$options.name, "makeTop Result:", this.topLefts, this.topCenters, this.topRights);
      }
    },
    makeBody: function (bodys, lambdaData) {
      for (var body of bodys) {
        var component = {};
        component.name = `${body.name}`;
        component.ref = `${body.ref}`; 
        component.props = body.props;
        component.style = `${body.style}`;
        this.bodys.push(component);
      }
      this.$debug(this.$options.name, "makeBody", this.bodys);
      this.$nextTick()
      .then(() => {
        if (lambdaData) {
          if (lambdaData.where === "body") {
            this.$refs[`${lambdaData.ref}`][0][lambdaData.function](lambdaData.params, this.propertyValue);
          }
        }
      })
    },
    makeFooter: function (footers, lambdaData) {
      for (var footer of footers) {
        var component = {};
        component.name = `${footer.name}`;
        component.ref = `${footer.ref}`; 
        component.props = footer.props;
        component.style = `${footer.style}`;
        if (footer.align.toLowerCase() === "left") {
          this.footerLefts.push(component);
        } else if (footer.align.toLowerCase() === "center") {
          this.footerCenters.push(component);
        } else {
          this.footerRights.push(component);
        }
      this.$debug(this.$options.name, "makeFooter", this.footerLefts, this.footerCenters, this.footerRights);
        this.$nextTick()
        .then(() => {
          if (lambdaData) {
            if (lambdaData.where === "footer") {
              this.$refs[`${lambdaData.ref}`][0][lambdaData.function](lambdaData.params, this.propertyValue);
            }
          }
        })
      }
    },
    signalData: function (data, ref, des) {
      this.$refs[ref][0][des](data);
    },
    transData: function (data, ref, des) {
      this.$refs[ref][0][des](data);
    },
    writeSuccess: function ($data) {
      this.$emit("writeSuccess", $data);
    }
  },
  created() {
    var meta = require("@/components/LambdaWidget/test/metadata.json")['info']['meta'];
    // var meta = this.metaData;
    var lambdaData = null;
    if (meta.info) {
      if (meta.info.lambdaData) {
        lambdaData = meta.info.lambdaData;
      }
    }
    if (meta.components.body) {
      this.$nextTick()
      .then(() => {
        this.makeBody(meta.components.body, lambdaData);
      })
    }
    if (meta.components.top) {
      setTimeout(() => {
        this.makeTop(meta.components.top, lambdaData);
      }, 1000)
    }
    if (meta.components.footer) {
      setTimeout(() => {
        this.makeFooter(meta.components.footer, lambdaData);
      }, 1000)
    }
  },
  mounted() {}
};
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
