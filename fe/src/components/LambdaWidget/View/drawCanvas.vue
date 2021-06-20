<template>
  <div class="canvasZone" ref="canvasZone">
    <canvas class="guideline" ref="guideline"></canvas>
    <canvas class="cache" ref="cache"></canvas>
    <canvas class="canvas" ref="canvas" v-resize.quiet="onResizeEnd"></canvas>

    <move-panel
      :x="0"
      :y="0"
      :w="movePanelWidth"
      :h="31"
      :parent="true"
      :draggable="true"
      :drag-handle="'.moveZone'"
      :resizable="false"
      :useOptionbutton="false"
    >
      <div class="optionZone">
        <div
          v-if="isUseShape('line')"
          class="option text-center"
          @click="setMode('line')"
        >
          <v-icon
            size="22"
            :color="mode === 'line' ? 'info' : undefined"
            :title="$t('drawcanvas.line')"
            >show_chart</v-icon
          >
        </div>
        <div
          v-if="isUseShape('rectangle')"
          class="option text-center"
          @click="setMode('rectangle')"
        >
          <v-icon
            size="22"
            :color="mode === 'rectangle' ? 'info' : undefined"
            :title="$t('drawcanvas.rectangle')"
            >crop_din</v-icon
          >
        </div>
        <div
          v-if="isUseShape('circle')"
          class="option text-center"
          @click="setMode('circle')"
        >
          <v-icon
            size="22"
            :color="mode === 'circle' ? 'info' : undefined"
            :title="$t('drawcanvas.circle')"
            >brightness_1</v-icon
          >
        </div>
        <div
          v-if="isUseShape('polygon')"
          class="option text-center"
          @click="setMode('polygon')"
        >
          <v-icon
            size="22"
            :color="mode === 'polygon' ? 'info' : undefined"
            :title="$t('drawcanvas.polygon')"
            >fas fa-draw-polygon</v-icon
          >
        </div>
        <div class="option text-center" @click="setMode('delete')">
          <v-icon size="22" :title="$t('drawcanvas.delete')">delete</v-icon>
        </div>
        <div class="option text-center" @click="onoffGuidline">
          <v-icon size="22" :title="$t('drawcanvas.guideline')"
            >border_clear</v-icon
          >
        </div>
        <div class="moveZone"></div>
      </div>
    </move-panel>
  </div>
</template>

<script>
import { Point } from "@/components/Graph/BaseRois.ts";

export default {
  name: "drawCanvas",
  props: {
    imgSize: {
      type: Array,
      default: undefined
    },
    originPoint: {
      type: Boolean,
      default: false
    },
    useShapes: {
      type: Array,
      default() {
        // return ["line", "rectangle", "circle", "polygon"]
        return ["line", "rectangle"]; // Not supported circle polygon.
      }
    },
    limitShape: {
      type: Number,
      default: -1
    },
    returnType: {
      type: String,
      default: "csv"
    }
  },
  components: {},
  data() {
    return {
      // canvas element with context.
      g_cvs: null,
      g_ctx: null,
      c_cvs: null,
      c_ctx: null,
      cvs: null,
      ctx: null,

      // draw mode.
      mode: null,

      // pointer.
      cachePointer: {},

      // shapes info.
      lines: [], // {type: lines [[x1,y1, x2,y2], [x1,y1, x2,y2]]
      rects: [], // [[x,y,w,h], [x,y,w,h]]
      circles: [], // [[x,y,w,h], [x,y,w,h]]
      polygons: [], // [[x1,y1, x2,y2, x3,y3], [x1,y1, x2,y2, x3,y3, x4,y4]]

      // guide line on off.
      useGuideline: true,

      // resize end event.
      resizeEnd: null
    };
  },
  computed: {
    shapes() {
      var shapes = {};
      shapes.lines = this.lines.slice();
      shapes.rects = this.rects.slice();
      shapes.circles = this.circles.slice();
      shapes.polygons = this.polygons.slice();
      return shapes;
    },
    movePanelWidth() {
      if (this.useShapes.length === 0) {
        return 59;
      } else if (this.useShapes.length === 1) {
        return 94;
      } else if (this.useShapes.length === 2) {
        return 119;
      } else if (this.useShapes.length === 3) {
        return 144;
      } else {
        return 169;
      }
    },
    returnCsvRectangles() {
      var result = "";
      if (this.rects.length > 0) {
        for (var i = 0; i < this.rects.length - 1; ++i) {
          result += this.rects[i].toString() + ",";
        }
        result += this.rects[this.rects.length - 1].toString();
      }
      return result;
    },
    returnCsvPolygons() {
      var result = "";
      if (this.polygons.length > 0) {
        for (var i = 0; i < this.polygons.length - 1; ++i) {
          result += this.polygons[i].toString() + "\n";
        }
        result += this.polygons[this.polygons.length - 1].toString();
      }
      return result;
    }
  },
  watch: {
    shapes: {
      immediate: true,
      deep: true,
      handler() {
        this.canvasClear(false);
        if (this.shapes.lines) {
          if (this.shapes.lines.length > 0) {
            for (let i = 0; i < this.shapes.lines.length; ++i) {
              // draw line.
              var line = this.exportLine(this.shapes.lines[i]);
              this.ctx.beginPath();
              this.ctx.moveTo(line[0], line[1]);
              this.ctx.lineTo(line[2], line[3]);
              this.ctx.closePath();
              this.ctx.stroke();
            }
          }
        }
        if (this.shapes.rects) {
          if (this.shapes.rects.length > 0) {
            for (let i = 0; i < this.shapes.rects.length; ++i) {
              // draw rect.
              var rect = this.exportRect(this.shapes.rects[i]);
              this.ctx.beginPath();
              this.ctx.rect(rect[0], rect[1], rect[2], rect[3]);
              this.ctx.closePath();
              this.ctx.stroke();
            }
          }
        }
        if (this.shapes.circles) {
          if (this.shapes.circles.length > 0) {
            for (let i = 0; i < this.shapes.circles.length; ++i) {
              // draw circle.
            }
          }
        }
        if (this.shapes.polygons) {
          if (this.shapes.polygons.length > 0) {
            for (let i = 0; i < this.shapes.polygons.length; ++i) {
              var polygon = this.exportPolygon(this.shapes.polygons[i]);
              this.ctx.beginPath();
              this.ctx.moveTo(polygon[0], polygon[1]);
              for (let i = 2; i < polygon.length; i += 2) {
                this.ctx.lineTo(polygon[i], polygon[i + 1]);
              }
              this.ctx.closePath();
              this.ctx.stroke();
              // draw polygon.
            }
          }
        }
        if (this.originPoint) {
          if (this.imgSize) {
            // cvt origin point value.
            // emit.
          }
        } else {
        }
        this.$emit("change", this.shapes);
      }
    }
  },
  methods: {
    /**
     * Check used shapes.
     * @public
     * @param {string} - shapes name.
     */
    isUseShape: function(shape) {
      var find = this.useShapes.indexOf(shape);
      if (find < 0) {
        return false;
      } else {
        return true;
      }
    },

    /**
     * Make canvas context.
     * @public
     */
    makePainter: function() {
      var ratio =
        this.$refs.canvasZone.clientHeight / this.$refs.canvasZone.clientWidth;
      // guideline canvas setting.
      this.g_cvs = this.$refs.guideline;
      this.g_cvs.width = this.$refs.canvasZone.clientWidth;
      this.g_cvs.height = this.$refs.canvasZone.clientHeight;
      this.g_ctx = this.g_cvs.getContext("2d");
      this.g_ctx.lineWidth = 2;
      this.g_ctx.strokeStyle = "grey";
      this.g_ctx.setLineDash([5, 5]);

      // cache canvas setting.
      this.c_cvs = this.$refs.cache;
      this.c_cvs.width = this.$refs.canvasZone.clientWidth;
      this.c_cvs.height = this.$refs.canvasZone.clientHeight;
      this.c_ctx = this.c_cvs.getContext("2d");
      this.c_ctx.lineWidth = 2;
      this.c_ctx.strokeStyle = "cyan";

      // real canvas setting.
      this.cvs = this.$refs.canvas;
      this.cvs.width = this.$refs.canvasZone.clientWidth;
      this.cvs.height = this.$refs.canvasZone.clientHeight;
      this.ctx = this.cvs.getContext("2d");
      this.ctx.lineWidth = 2;
      this.ctx.strokeStyle = "rgb(0,0,255)";

      // Auto shape mode.
      if (this.useShapes.length >= 1) {
        this.setMode(this.useShapes[0]);
      } else {
        alert(
          "Empty draw mode. Please insert shape mode ['line', 'rectangle']"
        );
      }

      this.ctx.imageSmoothingEnabled = this.ctx.mozImageSmoothingEnabled = this.ctx.imageSmoothingEnabled = true;
      // Make mouse event.
      this.cvs.addEventListener("pointerdown", this.drawStart);
      this.cvs.addEventListener("pointermove", this.drawing);
      this.cvs.addEventListener("pointerup", this.drawEnd);
      window.addEventListener("keypress", this.onEnter, false);
    },

    /**
     * Initilaize canvas.
     * @public
     */
    created: function() {
      if (this.$refs.canvas) {
        this.makePainter();
      } else {
        this.$error(this.$options.name, "created", "Not found canvas.");
      }
    },

    /**
     * Set draw mode. (line, rectangle, circle, polygon)
     * @public
     * @param {string} - drawing mode.
     */
    setMode: function(mode) {
      if (mode === "delete") {
        // all clear.
        this.allClear(true);
        return;
      }
      this.mode = mode;
    },

    /**
     * Mouse down event -> Draw start.
     * @public
     * @param {object} - mouse event data.
     */
    drawStart: function($pointer) {
      // save first point at cache.
      this.cvs.setPointerCapture($pointer.pointerId);
      switch (this.mode) {
        case "line": {
          this.cachePointer.x1 = $pointer.offsetX;
          this.cachePointer.y1 = $pointer.offsetY;
          break;
        }
        case "rectangle": {
          this.cachePointer.x = $pointer.offsetX;
          this.cachePointer.y = $pointer.offsetY;
          break;
        }
      }
    },

    /**
     * Mouse down event -> Draw start.
     * @public
     * @param {object} - mouse event data.
     */
    drawing: function($pointer) {
      // guideline drawing.
      var offsetX = $pointer.offsetX;
      var offsetY = $pointer.offsetY;
      if (offsetX < 0) {
        offsetX = 0;
      } else if (offsetX > this.cvs.width) {
        offsetX = this.cvs.width;
      }
      if (offsetY < 0) {
        offsetY = 0;
      } else if (offsetY > this.cvs.height) {
        offsetY = this.cvs.height;
      }
      if (this.useGuideline) {
        this.guidelineClear();
        this.g_ctx.beginPath();
        this.g_ctx.moveTo(0, offsetY);
        this.g_ctx.lineTo(this.g_cvs.width, offsetY);
        this.g_ctx.stroke();
        this.g_ctx.closePath();

        this.g_ctx.beginPath();
        this.g_ctx.moveTo(offsetX, 0);
        this.g_ctx.lineTo(offsetX, this.g_cvs.height);
        this.g_ctx.stroke();
        this.g_ctx.closePath();
      }

      // cache clear and drawing.
      switch (this.mode) {
        case "line": {
          if (!(this.cachePointer.x1 && this.cachePointer.y1)) {
            break;
          }
          if (this.limitShape > 0) {
            if (this.lines.length >= this.limitShape) {
              break;
            }
          }
          this.cacheClear();
          this.cachePointer.x2 = offsetX;
          this.cachePointer.y2 = offsetY;
          this.c_ctx.beginPath();
          this.c_ctx.moveTo(this.cachePointer.x1, this.cachePointer.y1);
          this.c_ctx.lineTo(this.cachePointer.x2, this.cachePointer.y2);
          this.c_ctx.stroke();
          this.c_ctx.closePath();
          break;
        }
        case "rectangle": {
          if (!(this.cachePointer.x && this.cachePointer.y)) {
            break;
          }
          if (this.limitShape > 0) {
            if (this.rects.length >= this.limitShape) {
              break;
            }
          }
          this.cacheClear();
          this.cachePointer.w = offsetX - this.cachePointer.x;
          this.cachePointer.h = offsetY - this.cachePointer.y;
          this.c_ctx.beginPath();
          this.c_ctx.rect(
            this.cachePointer.x,
            this.cachePointer.y,
            this.cachePointer.w,
            this.cachePointer.h
          );
          this.c_ctx.stroke();
          this.c_ctx.closePath();
          break;
        }
        case "polygon": {
          if (!this.cachePointer.point) {
            break;
          } else {
            this.cacheClear();
            if (this.cachePointer.point.length >= 2) {
              this.c_ctx.beginPath();
              this.c_ctx.moveTo(
                this.cachePointer.point[0],
                this.cachePointer.point[1]
              );
              for (let i = 2; i < this.cachePointer.point.length; i += 2) {
                this.c_ctx.lineTo(
                  this.cachePointer.point[i],
                  this.cachePointer.point[i + 1]
                );
              }
              this.c_ctx.lineTo($pointer.offsetX, $pointer.offsetY);
              // this.c_ctx.closePath(); // 다각형으로 그려지게 한다.
              this.c_ctx.stroke();
            }
          }
          break;
        }
      }
    },

    /**
     * Mouse down event -> Draw start.
     * @public
     * @param {object} - mouse event data.
     */
    drawEnd: function($pointer) {
      // cache clear -> insert shapes relative value data.
      switch (this.mode) {
        case "line": {
          if (
            !(
              this.cachePointer.x1 &&
              this.cachePointer.y1 &&
              this.cachePointer.x2 &&
              this.cachePointer.y2
            )
          ) {
            this.cachePointer = {};
            break;
          }
          // this.lines.push([this.cachePointer.x1, this.cachePointer.y1, this.cachePointer.x2, this.cachePointer.y2])
          this.insertLine([
            this.cachePointer.x1,
            this.cachePointer.y1,
            this.cachePointer.x2,
            this.cachePointer.y2
          ]);
          this.$debug(
            "canvas",
            "drawline",
            this.cachePointer.x1,
            this.cachePointer.y1,
            this.cachePointer.x2,
            this.cachePointer.y2
          );
          this.cacheClear();
          this.cachePointer = {};
          break;
        }
        case "rectangle": {
          if (
            !(
              this.cachePointer.x &&
              this.cachePointer.y &&
              this.cachePointer.w &&
              this.cachePointer.h
            )
          ) {
            this.cachePointer = {};
            break;
          }
          if (this.cachePointer.w < 0) {
            this.cachePointer.x = this.cachePointer.x + this.cachePointer.w;
            this.cachePointer.w *= -1;
          }
          if (this.cachePointer.h < 0) {
            this.cachePointer.y = this.cachePointer.y + this.cachePointer.h;
            this.cachePointer.h *= -1;
          }
          // this.rects.push([this.cachePointer.x, this.cachePointer.y, this.cachePointer.w, this.cachePointer.h])
          this.insertRect([
            this.cachePointer.x,
            this.cachePointer.y,
            this.cachePointer.w,
            this.cachePointer.h
          ]);
          this.$debug(
            "canvas",
            "rect",
            this.cachePointer.x,
            this.cachePointer.y,
            this.cachePointer.w,
            this.cachePointer.h
          );
          this.cacheClear();
          this.cachePointer = {};
          break;
        }
        case "polygon": {
          if (this.limitShape > 0) {
            if (this.polygons.length >= this.limitShape) {
              break;
            }
          }
          if (!this.cachePointer.point) {
            this.cachePointer.point = [];
            this.cachePointer.point.push($pointer.offsetX);
            this.cachePointer.point.push($pointer.offsetY);
          } else {
            this.cachePointer.point.push($pointer.offsetX);
            this.cachePointer.point.push($pointer.offsetY);
          }
          break;
        }
      }
      this.cvs.releasePointerCapture($pointer.pointerId);
    },

    /**
     * Insert line data.
     * @public
     * @param {array} - line data.
     */
    insertLine: function(line) {
      line[0] = this.convertStaticToRelative(line[0]);
      line[1] = this.convertStaticToRelative(line[1], "height");
      line[2] = this.convertStaticToRelative(line[2]);
      line[3] = this.convertStaticToRelative(line[3], "height");
      this.lines.push(line);
    },

    /**
     * Export convert Relative line value to Static line value.
     * @public
     * @param {array} - relative line value.
     */
    exportLine: function(relativeLine) {
      var exportLine = relativeLine.slice();
      exportLine[0] = this.convertRelativeToStatic(exportLine[0]);
      exportLine[1] = this.convertRelativeToStatic(exportLine[1], "height");
      exportLine[2] = this.convertRelativeToStatic(exportLine[2]);
      exportLine[3] = this.convertRelativeToStatic(exportLine[3], "height");
      return exportLine;
    },

    /**
     * Insert rectangle data.
     * @public
     * @param {array} - rectangle data.
     */
    insertRect: function(rect) {
      rect[0] = this.convertStaticToRelative(rect[0]);
      rect[1] = this.convertStaticToRelative(rect[1], "height");
      rect[2] = this.convertStaticToRelative(rect[2]);
      rect[3] = this.convertStaticToRelative(rect[3], "height");
      this.rects.push(rect);
    },

    /**
     * Export convert Relative rect value to Static rect value.
     * @public
     * @param {array} - relative rect value.
     */
    exportRect: function(relativeRect) {
      var exportRect = relativeRect.slice();
      exportRect[0] = this.convertRelativeToStatic(exportRect[0]);
      exportRect[1] = this.convertRelativeToStatic(exportRect[1], "height");
      exportRect[2] = this.convertRelativeToStatic(exportRect[2]);
      exportRect[3] = this.convertRelativeToStatic(exportRect[3], "height");
      return exportRect;
    },

    /**
     * Insert circle data.
     * @public
     * @param {array} - circle data.
     */
    insertCircle: function(circle) {
      circle[0] = this.convertStaticToRelative(circle[0]);
      circle[1] = this.convertStaticToRelative(circle[1], "height");
      circle[2] = this.convertStaticToRelative(circle[2]);
      circle[3] = this.convertStaticToRelative(circle[3], "height");
      this.circles.push(cirlce);
    },

    /**
     * Export convert Relative circle value to Static circle value.
     * @public
     * @param {array} - relative circle value.
     */
    exportCircle: function(relativeCircle) {
      var exportCircle = relativeCircle.slice();
      exportCircle[0] = this.convertRelativeToStatic(exportCircle[0]);
      exportCircle[1] = this.convertRelativeToStatic(exportCircle[1], "height");
      exportCircle[2] = this.convertRelativeToStatic(exportCircle[2]);
      exportCircle[3] = this.convertRelativeToStatic(exportCircle[3], "height");
      return exportCircle;
    },

    /**
     * Insert polygon data.
     * @public
     * @param {array} - polygon data.
     */
    insertPolygon: function(polygon) {
      for (var i = 0; i < polygon.length; i += 2) {
        polygon[i] = this.convertStaticToRelative(polygon[i]);
      }
      for (var i = 1; i < polygon.length; i += 2) {
        polygon[i] = this.convertStaticToRelative(polygon[i], "height");
      }
      this.polygons.push(polygon);
    },

    /**
     * Export convert Relative circle value to Static circle value.
     * @public
     * @param {array} - relative polygon value.
     */
    exportPolygon: function(relativePolygon) {
      var exportPolygon = relativePolygon.slice();
      for (var i = 0; i < exportPolygon.length; i += 2) {
        exportPolygon[i] = this.convertRelativeToStatic(exportPolygon[i]);
      }
      for (var i = 1; i < exportPolygon.length; i += 2) {
        exportPolygon[i] = this.convertRelativeToStatic(
          exportPolygon[i],
          "height"
        );
      }
      return exportPolygon;
    },

    /**
     * Cache canvas clear.
     * @public
     */
    cacheClear: function() {
      this.c_ctx.clearRect(0, 0, this.c_cvs.width, this.c_cvs.height);
    },

    /**
     * Guideline canvas clear.
     * @public
     */
    guidelineClear: function() {
      this.g_ctx.clearRect(0, 0, this.g_cvs.width, this.g_cvs.height);
    },

    /**
     * Canvas clear.
     * @public
     * @param {boolean} - clear canvas shapes data.
     */
    canvasClear: function(isClearData) {
      if (isClearData) {
        this.lines = [];
        this.rects = [];
        this.circles = [];
        this.polygons = [];
        this.$debug(this.$options.name, "canvasClear", "Shapes:", this.shapes);
      }
      if (this.ctx) {
        this.ctx.clearRect(0, 0, this.cvs.width, this.cvs.height);
      }
    },

    /**
     * Cache canvas and Canvas clear.
     * @public
     * @param {boolean} - clear canvas shapes data.
     */
    allClear: function(isClearData) {
      this.cacheClear();
      this.canvasClear(isClearData);
      this.$emit("clear");
    },

    convertRelativeToStatic: function(value, type) {
      var t = type || "width";
      if (t === "width") {
        // width ..
        return value * this.cvs.width;
      } else {
        // height ..
        return value * this.cvs.height;
      }
    },

    convertStaticToRelative: function(value, type) {
      var t = type || "width";
      if (t === "width") {
        // width ..
        return value / this.cvs.width;
      } else {
        // height ..
        return value / this.cvs.height;
      }
    },

    onoffGuidline: function() {
      this.useGuideline = !this.useGuideline;
      this.guidelineClear();
    },

    onResizeEnd: function($event) {
      if (this.resizeEnd) {
        clearTimeout(this.resizeEnd);
        this.resizeEnd = null;
      }
      this.resizeEnd = setTimeout(() => {
        this.makePainter();
        var copy = this.rects.slice();
        this.rects.length = 0;
        this.$nextTick().then(() => {
          this.rects = [...copy];
        });
        this.$debug(this.$options.name, "onResizeEnd", "Resize End Evnet!!");
      }, 400);
    },

    // setLine, setCircle, setPolygon...
    addRectangles: function(data) {
      var stride = 4;
      if (!data) {
        return;
      }
      if (typeof data === "string") {
        var spt = data.split(",");
        var rect = [];
        var count = 0;
        if (spt.length < 4) {
          this.$error(
            this.$options.name,
            "addRectangles",
            "Wrong params.",
            data
          );
          return;
        }
        for (var i = 0; i < spt.length; ++i) {
          rect.push(spt[i]);
          ++count;
          if (count === stride) {
            if (this.limitShape > 0) {
              if (this.rects.length >= this.limitShape) {
                this.$warn(
                  this.$options.name,
                  "addRectangles",
                  "number of rectangle limit exceeded. Limit:",
                  this.limitShape,
                  "Rectangles:",
                  this.rects.length
                );
                break;
              }
            }
            this.rects.push(rect);
            rect = [];
            count = 0;
          }
        }
      }
    },
    setRectangles: function(data) {
      var stride = 4;
      if (!data) {
        return;
      }
      if (typeof data === "string") {
        var spt = data.split(",");
        var rect = [];
        var count = 0;
        if (spt.length < 4) {
          this.$error(
            this.$options.name,
            "setRectangles",
            "Wrong params.",
            data
          );
          return;
        }
        this.rects.length = 0;
        for (var i = 0; i < spt.length; ++i) {
          rect.push(spt[i]);
          ++count;
          if (count === stride) {
            if (this.limitShape > 0) {
              if (this.rects.length >= this.limitShape) {
                this.$warn(
                  this.$options.name,
                  "addRectangles",
                  "number of rectangle limit exceeded. Limit:",
                  this.limitShape,
                  "Rectangles:",
                  this.rects.length
                );
                break;
              }
            }
            this.rects.push(rect);
            rect = [];
            count = 0;
          }
        }
      }
    },
    getRectangles: function() {
      var type = this.returnType;
      if (type === "csv") {
        return this.returnCsvRectangles;
      } else {
        return this.rects;
      }
    },
    addPolygon: function(data) {
      if (!data) {
        return;
      }
      if (typeof data === "string") {
        var spt = data.split(",");
        var polygon = [];
        const limited_location = 6;

        if (spt.length < limited_location) {
          this.$error(this.$options.name, "addPolygon", "Wrong params.", data);
          return;
        }
        for (var i = 0; i < spt.length; ++i) {
          if (this.limitShape > 0) {
            if (this.polygons.length >= this.limitShape) {
              this.$warn(
                this.$options.name,
                "addPolygon",
                "number of polygon limit exceeded. Limit:",
                this.limitShape,
                "Polygons:",
                this.polygons.length
              );
              break;
            }
          }
          polygon.push(spt[i]);
        }
        this.polygons.push(polygon);
        polygon = [];
      }
    },
    setAppPolygons: function(datas) {},

    setStrokeEndStyle: function(color) {
      this.ctx.strokeStyle = "rgb(" + color[0] + "," + color[1] + "," + color[2] + ")";
    },

    setPolygons: function(datas) {
      if (!datas) {
        this.$warn(this.$options.name, "setPolygons", "Wrong datas", datas);
        return;
      }

      try {
        datas = JSON.parse(datas);
        var temp = [];
        for (var i = 0; i < datas.length; ++i) {
          temp.push(datas[i].join(","));
        }
        datas = temp;
      } catch {
        if (datas.includes("\n")) {
          datas = datas.split("\n");
        }
      }
      this.polygons = [];
      for (var i = 0; i < datas.length; ++i) {
        var polygon = datas[i];
        this.addPolygon(polygon);
      }
    },

    getPolygons: function() {
      var type = this.returnType;
      if (type === "csv") {
        return this.returnCsvPolygons;
      } else {
        return this.polygons;
      }
    },
    onEnter: function($key) {
      if ($key.keyCode !== 13) {
        return;
      }
      if (this.mode === "polygon") {
        if (this.cachePointer.point) {
          if (this.cachePointer.point.length > 2) {
            this.insertPolygon(this.cachePointer.point);
            this.cachePointer = {};
            this.cacheClear();
          } else {
            this.cachePointer = {};
            this.cacheClear();
          }
        }
      }
      this.$emit("rois", this.polygons);
    }
  },
  created() {},
  mounted() {
    this.$nextTick().then(() => {
      this.created();
    });
  },
  beforeDestroy() {
    this.cvs.removeEventListener("pointerdown", this.drawStart);
    this.cvs.removeEventListener("pointermove", this.drawing);
    this.cvs.removeEventListener("pointerup", this.drawEnd);
    window.removeEventListener("keypress", this.onEnter);
  }
};
</script>

<style scoped>
.canvasZone {
  display: inline-block;
  position: absolute;
  width: 100%;
  height: 100%;
}
.guideline {
  position: absolute;
  width: 100%;
  height: 100%;
}
.cache {
  position: absolute;
  width: 100%;
  height: 100%;
}
.canvas {
  position: absolute;
  width: 100%;
  height: 100%;
}
.optionZone {
  float: left;
  width: 100%;
  height: 100%;
}
.option {
  float: left;
  width: 25px;
  height: 25px;
  cursor: pointer;
}
.moveZone {
  background-color: rgba(125, 125, 125, 0.8);
  cursor: move;
  width: 15px;
  height: 100%;
  position: absolute;
  right: 0px;
}
</style>
