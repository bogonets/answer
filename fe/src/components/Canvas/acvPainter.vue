<template>
  <div id="main" ref="main" v-resize.quiet="onResize">
    <audio ref="alarm">
      <source src="@/assets/beep-1.wav">
    </audio>
    <canvas 
    id="cache"
    ref="cache"
    ></canvas>
    <canvas 
    id="real"  
    ref="real"  
    @contextmenu="onContext"
    @click="onClick($event)"
    @dblclick="onDBClick($event)"></canvas>
    <v-btn-toggle v-if="edit">
      <v-tooltip bottom>
				<template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="changeType('line')"><v-icon>show_chart</v-icon></v-btn>
				</template>
        <span>draw_line</span>
      </v-tooltip>
      <v-tooltip bottom>
				<template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="changeType('rect')"><v-icon>crop_din</v-icon></v-btn>
				</template>
        <span>draw_rect</span>
      </v-tooltip>
      <v-tooltip bottom>
				<template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="changeType('arc')"><v-icon>brightness_1</v-icon></v-btn>
				</template>
        <span>draw_circle</span>
      </v-tooltip>
      <v-tooltip bottom>
				<template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="changeType('polygon')"><v-icon>category</v-icon></v-btn>
				</template>
        <span>draw_polygon</span>
      </v-tooltip>
      <v-tooltip bottom>
				<template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="clearAll"><v-icon>delete</v-icon></v-btn>
				</template>
        <span>clear_all</span>
      </v-tooltip>
    </v-btn-toggle>
    <v-snackbar v-model="alert" top right absolute :timeout="5000">
			<span style="color: orange;">{{ $t('mode') + ' : ' + $t(draw_type) }}</span>
			<v-btn text @click="alert = !alert">{{$t('close')}}</v-btn>
		</v-snackbar>
  </div>
</template>

<script>
/**
 * Painter component.
 * @author hadoo
 */
import * as Painter from "@/services/paint";
export default {
  props:{
    /**
     * This Component Use value.
     */
    edit: {
      type: Boolean,
      default: false
    },
    /**
     * Event Area Show Value.
     */
    hide_event: {
      type: Boolean,
      default: false
    }
  },
  components:{
  },
  data(){
    return {
      name: "acvPainter",
      cache_canvas: null,
      cache_painter: null,
      real_canvas: null,
      real_painter: null,

      drag_state: false,
      draw_type: "",

      alert: false,

      draw_points: null,

      drawing_poly: false,
      draw_poly_points: [],

      rate_x: null,
      rate_y: null,

      lines: [],
      rects: [],
      polys: [],
      arcs : [],

      resizeTimer: null,
    }
  },
  computed:{

  },
  watch: {
    draw_type() {
			if (this.draw_type !== "clear" || this.draw_type !== "") {
				this.alert = true;
			}
    }
  },
  methods:{
    /**
		 * This component's initialize.
		 * @param {null}
		 * @public
		 */
    initialize: function () {
      if (!this.$refs.main) {
        return;
      }
      var ratio = this.$refs.main.clientHeight / this.$refs.main.clientWidth;
      this.cache_canvas = this.$refs.cache;
      this.cache_canvas.width = 1000;
      this.cache_canvas.height = ratio * this.cache_canvas.width;
      this.cache_painter = this.cache_canvas.getContext("2d");
      this.real_canvas = this.$refs.real;
      this.real_canvas.width = 1000;
      this.real_canvas.height = ratio * this.real_canvas.width;
      this.real_painter = this.real_canvas.getContext("2d");
      this.rate_x = this.cache_canvas.width / this.$refs.main.clientWidth;
      this.rate_y = this.cache_canvas.height / this.$refs.main.clientHeight;
      if (this.real_canvas) {
        this.real_canvas.onpointerdown = this.onDragStart;
        this.real_canvas.onpointermove = this.onDrag;
        this.real_canvas.onpointerup = this.onDragEnd;
      } else {
        this.$warn(this.name, "initialize", "real canvas is", this.real_canvas);
      }
    },
    /**
		 * This component's Destroy.
		 * @param {null}
		 * @public
		 */
    destroy: function () {
      this.cache_canvas = null;
      this.cache_painter = null;
      this.real_canvas = null;
      this.real_painter = null;
      this.draw_type = "";
    },
    /**
		 * Type: lines, rects, arcs, polys. Change Draw Type.
		 * @param {null}
		 * @public
		 */
    changeType: function (type) {
      this.draw_type = type;
      this.drag_state = false;
      this.draw_points = null;
      this.drawing_poly = false;
      this.draw_poly_points = [];
    },
    /**
		 * Alarm Event.
		 * @param {null}
		 * @public
		 */
    onBeep: function () {
      if (this.$refs.alarm) {
        this.$refs.alarm.play();
      } else {
        this.$warn(this.name, "onBeep", "Alarm is not mounted.");
      }
    },
    /**
		 * Prevent ContextMenu Event.
		 * @param {contextEvent}
		 * @public
		 */
    onContext: function (event) {
      event.preventDefault();
    },
    /**
		 * Drag Start Event. Start Drawing.
		 * @param {mouseEvent}
		 * @public
		 */
    onDragStart: function (event) {
      if (this.draw_type === "") {
        return;
      }
      this.real_canvas.setPointerCapture(event.pointerId);
      this.drag_state = true;
      this.draw_points = {};
      this.draw_points.first_point = {};
      this.draw_points.first_point.x = event.offsetX * this.rate_x;
      this.draw_points.first_point.y = event.offsetY * this.rate_y;
    },
    /**
		 * Drag Event. Drawing Shape.
		 * @param {mouseEvent}
		 * @public
		 */
    onDrag: function (event) {
      if (this.drag_state) {
        var pointX = event.offsetX;
        var pointY = event.offsetY;
        if (pointX > this.real_canvas.clientWidth) {
          pointX = this.real_canvas.clientWidth;
        } else if (pointX < 0) {
          pointX = 0;
        }
        if (pointY > this.real_canvas.clientHeight) {
          pointY = this.real_canvas.clientHeight;
        } else if (pointY < 0) {
          pointY = 0;
        }
        Painter.clearAll(this.cache_painter, this.cache_canvas);
        if (this.draw_type === "line") {
          this.draw_points.second_point = {};
          this.draw_points.second_point.x = pointX * this.rate_x;
          this.draw_points.second_point.y = pointY * this.rate_y;
          Painter.drawLine(this.cache_painter, this.draw_points.first_point, this.draw_points.second_point, "red", 4);
        } else if (this.draw_type === "rect") {
          this.draw_points.second_point = {};
          this.draw_points.second_point.x = pointX * this.rate_x;
          this.draw_points.second_point.y = pointY * this.rate_y;
          var width = this.draw_points.second_point.x - this.draw_points.first_point.x;
          var height = this.draw_points.second_point.y - this.draw_points.first_point.y;
          Painter.drawRect(this.cache_painter, this.draw_points.first_point, width, height, "red", 4, false);
        } else if (this.draw_type === "arc") {
          this.draw_points.second_point = {};
          this.draw_points.second_point.x = pointX * this.rate_x;
          this.draw_points.second_point.y = pointY * this.rate_y;
          var width = Math.abs(this.draw_points.second_point.x - this.draw_points.first_point.x);
          var height = Math.abs(this.draw_points.second_point.y - this.draw_points.first_point.y);
          var radius = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2));
          Painter.drawArc(this.cache_painter, this.draw_points.first_point, radius, 0, 2, "red", 4, false);
        }
        return;
      } else if (this.drawing_poly) {
        if (this.draw_type === "polygon") {
          Painter.clearAll(this.cache_painter, this.cache_canvas);
          var last_point = {};
          last_point.x = pointX * this.rate_x;
          last_point.y = pointY * this.rate_y;
          Painter.drawPolyForCache(this.cache_painter, this.draw_poly_points, last_point, "red", 4, true, false);
        }
      }
    },
    /**
		 * Drag End Event. End drawing.
		 * @param {mouseEvent}
		 * @public
		 */
    onDragEnd: function (event) {
      if (!this.drag_state) {
        return;
      }
      var pointX = event.offsetX;
      var pointY = event.offsetY;
      if (pointX > this.real_canvas.clientWidth) {
        pointX = this.real_canvas.clientWidth;
      } else if (pointX < 0) {
        pointX = 0;
      }
      if (pointY > this.real_canvas.clientHeight) {
        pointY = this.real_canvas.clientHeight;
      } else if (pointY < 0) {
        pointY = 0;
      }
      this.drag_state = false;
      Painter.clearAll(this.cache_painter, this.cache_canvas);
      this.draw_points.second_point = {};
      this.draw_points.second_point.x = pointX * this.rate_x;
      this.draw_points.second_point.y = pointY * this.rate_y;
      if (this.draw_type === "line") {
        Painter.drawLine(this.real_painter, this.draw_points.first_point, this.draw_points.second_point, "blue", 4);
        this.draw_points.first_point.x = this.draw_points.first_point.x / this.real_canvas.width;
        this.draw_points.first_point.y = this.draw_points.first_point.y / this.real_canvas.height;
        this.draw_points.second_point.x = this.draw_points.second_point.x / this.real_canvas.width;
        this.draw_points.second_point.y = this.draw_points.second_point.y / this.real_canvas.height;
        this.lines.push(this.draw_points);
        this.$debug(this.name, "onDragEnd", "LINES:", this.lines);
      } else if (this.draw_type === "rect") {
        var rect = {};
        rect.first_point = this.draw_points.first_point;
        rect.width = this.draw_points.second_point.x - this.draw_points.first_point.x;
        rect.height = this.draw_points.second_point.y - this.draw_points.first_point.y;
        Painter.drawRect(this.real_painter, rect.first_point, rect.width, rect.height, "blue", 4, false);
        rect.first_point.x = rect.first_point.x / this.real_canvas.width;
        rect.first_point.y = rect.first_point.y / this.real_canvas.height;
        rect.width = rect.width / this.real_canvas.width;
        rect.height = rect.height / this.real_canvas.height;
        this.rects.push(rect);
        this.$debug(this.name, "onDragEnd", "RECTS:", this.rects);
      } else if (this.draw_type === "arc") {
        var arc = {};
        arc.center_point = this.draw_points.first_point;
        arc.width = this.draw_points.second_point.x - this.draw_points.first_point.x;
        arc.height = this.draw_points.second_point.y - this.draw_points.first_point.y;
        Painter.drawArcWithSize(this.real_painter, arc.center_point, arc.width, arc.height, 0, 2, "blue", 4, false);
        arc.center_point.x = arc.center_point.x / this.real_canvas.width;
        arc.center_point.y = arc.center_point.y / this.real_canvas.height;
        arc.width = arc.width / this.real_canvas.width;
        arc.height = arc.height / this.real_canvas.height;
        this.arcs.push(arc);
        this.$debug(this.name, "onDragEnd", "ARCS:", this.arcs);
      }
      this.real_canvas.releasePointerCapture(event.pointerId);
    },
    /**
		 * Click Event. Start Draw polygon or Drawing polygon.
		 * @param {mouseEvent}
		 * @public
		 */
    onClick: function (event) {
      if (this.draw_type !== "polygon") {
        return;
      }
      if (!this.drawing_poly) {
        this.draw_poly_points.legnth = 0;
        this.draw_poly_points.push({x: event.offsetX * this.rate_x, y: event.offsetY * this.rate_y});
        this.drawing_poly = true;
      } else {
        this.draw_poly_points.push({x: event.offsetX * this.rate_x, y: event.offsetY * this.rate_y});
      }
    },
    /**
		 * Double Click Event. End draw polygon.
		 * @param {mouseEvent}
		 * @public
		 */
    onDBClick: function (event) {
      if (this.draw_type !== "polygon") {
        return;
      }
      Painter.clearAll(this.cache_painter, this.cache_canvas);
      if (this.draw_poly_points.length > 0 ) {
        this.draw_poly_points.push({x: event.offsetX * this.rate_x, y: event.offsetY * this.rate_y});
        Painter.drawPoly(this.real_painter, this.draw_poly_points, "blue", 4, true, false);
        var poly = {};
        poly.points = [];
        for (var index = 0; index < this.draw_poly_points.length; ++index) {
          var point = this.draw_poly_points[index];
          point.x = point.x / this.real_canvas.width;
          point.y = point.y / this.real_canvas.height;
          poly.points.push(point);
        }
        this.polys.push(poly);
        this.drawing_poly = false;
        this.draw_poly_points = [];
        this.$debug(this.name, "onDBClick", "POLYS:", this.polys);
      }
    },
    /**
		 * Draw Line.
		 * @param {string} - Color name or Hex code.
		 * @public
		 */
    drawLines: function (color) {
      for (var index = 0; index < this.lines.length; ++index) {
        var line = this.lines[index];
        var first_point = {};
        first_point.x = line.first_point.x * this.real_canvas.width;
        first_point.y = line.first_point.y * this.real_canvas.height;
        var second_point = {};
        second_point.x = line.second_point.x * this.real_canvas.width;
        second_point.y = line.second_point.y * this.real_canvas.height;
        var line_color = "blue" || color;
        Painter.drawLine(this.real_painter, first_point, second_point, line_color, 4)
      }
    },
    /**
		 * Draw Rectangle.
		 * @param {string} - Color name or Hex code.
		 * @public
		 */
    drawRects: function (color) {
      for (var index = 0; index < this.rects.length; ++index) {
        var rect = this.rects[index];
        var left_top = {};
        left_top.x = rect.first_point.x * this.real_canvas.width;
        left_top.y = rect.first_point.y * this.real_canvas.height;
        var width = rect.width * this.real_canvas.width;
        var height = rect.height * this.real_canvas.height;
        var rect_color = "blue" || color || rect.color;
        Painter.drawRect(this.real_painter, left_top, width, height, rect_color, 4, false);
      }
    },
    /**
		 * Draw Arc.
		 * @param {string} - Color name or Hex code.
		 * @public
		 */
    drawArcs: function (color) {
      for (var index = 0; index < this.arcs.length; ++index) {
        var arc = this.arcs[index];
        var center_point = {};
        center_point.x = arc.center_point.x * this.real_canvas.width;
        center_point.y = arc.center_point.y * this.real_canvas.height;
        var width = arc.width * this.real_canvas.width;
        var height = arc.height * this.real_canvas.height;
        var arc_color = "blue" || color || arc.color;
        Painter.drawArcWithSize(this.real_painter, center_point, width, height, 0, 2, arc_color, 4, false);
      }
    },
    /**
		 * Draw Polygon.
		 * @param {string} - Color name or Hex code.
		 * @public
		 */
    drawPolys: function (color) {
      for (var index = 0; index < this.polys.length; ++index) {
        var poly = this.polys[index];
        var points = [];
        for (var i = 0; i < poly.points.length; ++i) {
          var point = poly.points[i];
          var x = point.x * this.real_canvas.width;
          var y = point.y * this.real_canvas.height;
          points.push({x: x, y: y}); 
        }
        var poly_color = "blue" || color || poly.color;
        Painter.drawPoly(this.real_painter, points, poly_color, 4, true, false);
      }
    },
    /**
		 * Clear All Shape.
		 * @param {null}
		 * @public
		 */
    clearAll: function () {
			Painter.clearAll(this.real_painter, this.real_canvas);
			Painter.clearAll(this.cache_painter, this.cache_canvas);
			this.draw_type = "clear_all";
      this.lines.length = 0;
      this.rects.length = 0;
      this.polys.length = 0;
      this.arcs.length  = 0;
    },
    /**
		 * Resize Event.
		 * @param {resizeEvent} - Resize event object.
		 * @public
		 */
    onResize: function (event) {
      var ratio = this.$refs.main.clientHeight / this.$refs.main.clientWidth;
      this.cache_canvas.width = 1000;
      this.cache_canvas.height = ratio * this.cache_canvas.width;
      this.real_canvas.width = 1000;
      this.real_canvas.height = ratio * this.real_canvas.width;
      this.rate_x = this.cache_canvas.width / this.$refs.main.clientWidth;
      this.rate_y = this.cache_canvas.height / this.$refs.main.clientHeight;
      Painter.clearAll(this.real_painter, this.real_canvas);
      this.drawLines();
      this.drawRects();
      this.drawArcs();
      this.drawPolys();
    },
    /**
		 * Get Draw Data.
		 * @param {null}
		 * @public
		 */
    // Util Methods.
    getData: function () {
      var result = {};
      // if (this.lines.length !== 0) {
      //   result.lines = this.lines;
      // }
      // if (this.rects.length !== 0) {
      //   result.rects = this.rects;
      // }
      // if (this.polys.length !== 0) {
      //   result.polys = this.polys;
      // }
      // if (this.arcs.length !== 0) {
      //   result.arcs = this.arcs;
      // }
      result.lines = this.lines.slice();
      result.rects = this.rects.slice();
      result.polys = this.polys.slice();
      result.arcs = this.arcs.slice();
      return result;
    },
    /**
		 * Draw Event Text.
		 * @param {string} - Color name or Hex code.
		 * @public
		 */
    drawEventResultText: function (event_text) {
      if (event_text) {
        if (event_text.includes(",")) {
          var temp = event_text.split(",");
          var text = temp[0] + this.$t(temp[1]);
          Painter.drawText(this.cache_painter, {x: 0, y: 50}, text, "red");
          return;
        }
        if (event_text === "warning") {
          this.onBeep();
        }
        Painter.drawText(this.cache_painter, {x: 0, y: 50}, event_text, "red");
      }
    },
    /**
		 * Draw Event Area.
		 * @param {object} - Event Area Object.
		 * @public
		 */
    drawEventArea: function (event_area) {
      for (var index = 0; index < event_area.length; ++index) {
        var color = event_area[index].color || "green";
        if (event_area[index].type === "lines") {
          for (var i = 0; i < event_area[index].points.length; ++i) {
            var line = event_area[index].points[i];
            var first_point = {};
            first_point.x = line[0] * this.cache_canvas.width;
            first_point.y = line[1] * this.cache_canvas.height;
            var second_point = {};
            second_point.x = line[2] * this.cache_canvas.width;
            second_point.y = line[3] * this.cache_canvas.height;
            Painter.drawLine(this.cache_painter, first_point, second_point, color, 4);
          }
        } else if (event_area[index].type === "rects") {
          for (var i = 0; i < event_area[index].points.length; ++i) {
            var rect = event_area[index].points[i];
            var first_point = {};
            first_point.x = rect[0] * this.cache_canvas.width;
            first_point.y = rect[1] * this.cache_canvas.height;
            var width = rect[2] * this.cache_canvas.width;
            var height = rect[3] * this.cache_canvas.height;
            Painter.drawRect(this.cache_painter, first_point, width, height, color, 4, false);
          }
        } else if (event_area[index].type === "polys") {
          for (var i = 0; i < event_area[index].points.length; ++i) {
            var poly = event_area[index].points[i];
            var poly_points = [];
            for (var poly_i = 0; poly_i < poly.length; poly_i += 2) {
              poly_points.push(poly[poly_i] * this.cache_canvas.width);
              poly_points.push(poly[poly_i + 1] * this.cache_canvas.height);
            }
            Painter.drawPoly(this.cache_painter, poly_points, color, 4, true, false);
          }
        } else if (event_area[index].type === "arcs") {
          for (var i = 0; i < event_area[index].points.length; ++i) {
            var arc = event_area[index].points[i];
            var center_point = {};
            center_point.x = arc[0] * this.cache_canvas.width;
            center_point.y = arc[1] * this.cache_canvas.height;
            var width = arc[2] * this.cache_canvas.width;
            var height = arc[3] * this.cache_canvas.height;
            Painter.drawArcWithSize(this.real_painter, center_point, width, height, 0, 2, color, 4, false);
          }
        }
      }
    },
    /**
		 * ConvertLines Data for API.
		 * @param {list} - Lines info list.
		 * @public
		 */
    convertLinesForAPI: function (lines) {
			var result = {};
			result.type = "lines";
			result.points = [];
			if (lines.length !== 0) {
				for (var i = 0; i < lines.length; ++i) {
					var line = lines[i];
					var point = []
					point.push(line.first_point.x);
					point.push(line.first_point.y);
					point.push(line.second_point.x);
					point.push(line.second_point.y);
					result.points.push(point);
				}
			}
			return result;
    },
    /**
		 * ConvertRects Data for API.
		 * @param {list} - rects info list.
		 * @public
		 */
		convertRectsForAPI: function (rects) {
			var result = {};
			result.type = "rects";
			result.points = [];
			if (rects.length !== 0) {
				for (var i = 0; i < rects.length; ++i) {
					var rect = rects[i];
					var value = []
					value.push(rect.first_point.x);
					value.push(rect.first_point.y);
					value.push(rect.width);
					value.push(rect.height);
					result.points.push(value);
				}
			}
			return result;
    },
    /**
		 * ConvertPolygons Data for API.
		 * @param {list} - polygons info list.
		 * @public
		 */
		convertPolysForAPI: function (polys) {
			var result = {};
			result.type = "polys";
			result.points = [];
			if (polys.length !== 0) {
				for (var i = 0; i < polys.length; ++i) {
					var poly = polys[i];
					var point = []
					for (var poly_i = 0; poly_i < poly.points.length; ++ poly_i) {
						point.push(poly.points[poly_i].x);
						point.push(poly.points[poly_i].y);
					}
					result.points.push(point);
				}
			}
			return result;
    },
    /**
		 * ConvertArcs Data for API.
		 * @param {list} - Arcs info list.
		 * @public
		 */
		convertArcsForAPI: function (arcs) {
			var result = {};
			result.type = "arcs";
			result.points = [];
			if (arcs.length !== 0) {
				for (var i = 0; i < arcs.length; ++i) {
					var arc = arcs[i];
					var value = []
					value.push(arc.center_point.x);
					value.push(arc.center_point.y);
					value.push(arc.width);
					value.push(arc.height);
					result.points.push(value);
				}
			}
			return result;
    },
    /**
		 * Load Preset Data.
		 * @param {object} - Presave data.
		 * @public
		 */
    loadPresetData: function (presave_data) {
      this.$nextTick(() => {
        var load_data = presave_data.event_area;
        if (load_data) {
          for (var index = 0; index < load_data.length; ++index) {
            if (load_data[index].type === "lines") {
              this.convertLinesData(load_data[index].points, load_data[index].color);
            } else if (load_data[index].type === "rects") {
              this.convertRectsData(load_data[index].points, load_data[index].color);
            } else if (load_data[index].type === "polys") {
              this.convertPolysData(load_data[index].points, load_data[index].color);
            } else if (load_data[index].type === "arcs") {
              this.convertArcsData(load_data[index].points, load_data[index].color);
            }
          }
        }
        this.drawLines();
        this.drawRects();
        this.drawArcs();
        this.drawPolys();
      })
    },
    /**
		 * Convert Lines Data for This Component.
		 * @param {list, string} - Lines Points list and Color Name or Hex code.
		 * @public
		 */
    convertLinesData: function (points, color) {
      if (points.length === 0) {
        return;
      }
      for (var index = 0; index < points.length; ++index) {
        var line = {};
        var predata_line = points[index];
        line.first_point  = {};
        line.second_point = {};
        line.first_point.x  = predata_line[0];
        line.first_point.y  = predata_line[1];
        line.second_point.x = predata_line[2];
        line.second_point.y = predata_line[3];
        line.color = color;
        this.lines.push(line);
        // if (type === "presave") {
        //   this.lines.push(line);
        // } else if (type === "drawing_event") {
        //   Painter.drawLine(this.cache_painter, this.draw_points.first_point, this.draw_points.second_point, "red", 4);
        //   Painter.drawLine(this.cache_painter, line.first_point, line.second_point, )
        // }
      }
    },
    /**
		 * Convert Rects Data for This Component.
		 * @param {list, string} - Rects Points list and Color Name or Hex code.
		 * @public
		 */
    convertRectsData: function (points, color) {
      if (points.length === 0) {
        return;
      }
      for (var index = 0; index < points.length; ++index) {
        var rect = {};
        var predata_rect = points[index];
        rect.first_point = {};
        rect.first_point.x = predata_rect[0];
        rect.first_point.y = predata_rect[1];
        rect.width  = predata_rect[2];
        rect.height = predata_rect[3];
        rect.color = color;
        this.rects.push(rect);
      }
    },
    /**
		 * Convert Polygons Data for This Component.
		 * @param {list, string} - Polygons Points list and Color Name or Hex code.
		 * @public
		 */
    convertPolysData: function (points, color) {
      if (points.length === 0) {
        return;
      }
      for (var index = 0; index < points.length; ++index) {
        var poly = {};
        poly.points = [];
        var predata_poly = points[index];
        for (var i = 0; i < predata_poly.length; i+=2) {
          poly.points.pusj({x: predata_poly[i], y: predata_poly[i+1]});
        }
        poly.color = color;
        this.polys.push(poly);
      }
    },
    /**
		 * Convert Arcs Data for This Component.
		 * @param {list, string} - Arcs Points list and Color Name or Hex code.
		 * @public
		 */
    convertArcsData: function (points, color) {
      if (points.length === 0) {
        return;
      }
      for (var index = 0; index < points.length; ++index) {
        var arc = {};
        var predata_arc = points[index];
        arc.center_point = {};
        arc.center_point.x = predata_arc[0];
        arc.center_point.y = predata_arc[1];
        arc.width  = predata_arc[2];
        arc.height = predata_arc[3];
        arc.color = color;
        this.arcs.push(arc);
      }
    },
    /**
		 * Draw Event.
		 * @param {JSON} - Draw Info Data.
		 * @public
		 */
    onEventDrawing: function (event) {
      var event_area_data = null;
      try {
        event_area_data = JSON.parse(event);
      } catch (err){
        this.$error(this.name, "onEventDrawing", "Json ParsingError", err);
      }
      Painter.clearAll(this.cache_painter, this.cache_canvas);
      if (event_area_data) {
        // this.$debug("DDD", event_area_data.data);
        if (event_area_data.data) {
          if (event_area_data.data.event_result) {
            this.drawEventResultText(event_area_data.data.event_result);
          }
          if (!this.hide_event) {
            if (event_area.data.event_area) {
              if (event_area_data.data.event_area.event_area) {
                this.drawEventArea(event_area_data.data.event_area.event_area);
              } else if (event_area_data.data.event_area) {
                this.drawEventArea(event_area_data.data.event_area);
              }
            }
          }
        }
      }
    }
  },
  created(){

  },
  mounted(){
    // this.initialize();
    this.$nextTick(() => { 
      this.initialize();
    })
    // setTimeout(this.initialize, 500);
  },
  beforeDestroy() {
    this.destroy(); 
  }
}
</script>

<style scoped>
#main {
  width: 100%;
  height: 100%;
}
#cache {
  position: absolute;
  width: 100%;
  height: 100%;
}
#real {
  position: absolute;
  width: 100%;
  height: 100%;
}
canvas {
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -o-user-select: none;
  user-select: none;
}
</style>