<template>
  <div style="width: 100%; height: 100%;">
    <window>
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
          >
          </component>
        </template>
      </template>
    </window>
  </div>
</template>

<script>
import Window from "@/components/Graph/test/RoisCanvasTemplateTest.vue";

// View
import viewText from "@/components/LambdaWidget/View/viewText.vue";
import viewImage from "@/components/LambdaWidget/View/viewImage.vue";
import drawCanvas from "@/components/LambdaWidget/View/drawCanvas.vue";

export default {
  name: "RoisCanvasTest",
  props: {
    lambdaProps: {
      default: undefined
    },
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
    viewText,
    viewImage,
    drawCanvas
  },
  data() {
    return {
      topLefts: [],
      topCenters: [],
      topRights: [],
      bodys: [],
      footerLefts: [],
      footerCenters: [],
      footerRights: []
    };
  },
  computed: {},
  methods: {
    makeTop: function(tops, lambdaData) {
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
    },
    makeBody: function(bodys, lambdaData) {
      for (var body of bodys) {
        var component = {};
        component.name = `${body.name}`;
        component.ref = `${body.ref}`;
        component.props = body.props;
        component.style = `${body.style}`;
        this.bodys.push(component);
      }
      this.$debug(this.$options.name, "makeBody", this.bodys);
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
    },
    makeFooter: function(footers, lambdaData) {
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
        this.$debug(
          this.$options.name,
          "makeFooter",
          this.footerLefts,
          this.footerCenters,
          this.footerRights
        );
        this.$nextTick().then(() => {
          if (lambdaData) {
            if (lambdaData.where === "footer") {
              this.$refs[`${lambdaData.ref}`][0][lambdaData.function](
                lambdaData.params,
                this.propertyValue
              );
            }
          }
        });
      }
    },
    signalData: function(data, ref, des) {
      this.$refs[ref][0][des](data);
    },
    transData: function(data, ref, des) {
      this.$refs[ref][0][des](data);
    },
    getSendData: function(ref, des) {
      try {
        return this.$refs[ref][0][des]();
      } catch {
        return ref; // In this case, it is a contant data.
      }
    },
    writeSuccess: function($data) {
      this.$emit("writeSuccess", $data);
    }
  },
  created() {
    var meta = {
      components: {
        body: [
          {
            name: "viewImage",
            ref: "image",
            style: ""
          },
          {
            name: "drawCanvas",
            props: { limitShape: 1, useShapes: ["polygon"] },
            ref: "canvas",
            style: ""
          }
        ]
      }
    };
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
  },
  mounted() {}
};
</script>
