<template>
	<div class="full-size">
		<canvas ref="vod_player"></canvas>
		<canvas class="drawing" ref="drawing"></canvas>
	</div>
</template>

<script>
/**
 * Video stream to Canvas image  For draw shape up vod.
 * @author hadoo
 */

import * as Painter from "@/services/paint";
import * as video_util from "@/services/videoToCanvas";
// import * as TEST from "@/components/Test/javascript/test.js";
import { setTimeout, clearTimeout } from "timers";
export default {
	props: {
		/**
		 * This VodPlayer Width.
		 */
		width: {
			type: Number,
			default: 1000
		},
		/**
		 * This VodPlayer Height.
		 */
		height: {
			type: Number,
			default: 1000
		},
		/**
		 * This VodPlayer Source.
		 */
		src: {
			type: String,
			default: ""
		},
		/**
		 * This VodPlayer Video Element.
		 */
		video: {
			type: Element,
			default: null
		},
		/**
		 * This VodPlayer Event Draw Type.
		 */
		draw_type: {
			type: String,
			default: null
		},
		/**
		 * Label Info list.
		 */
		label_setting: {
			type: Array,
			default: null
			// [{label: 'one', color: 'orange'}, {label: 'two', color: 'blue'}]
		}
	},
	components: {},
	data() {
		return {
			name: "acvVodPlayer",
			video_canvas: null,
			video_painter: null,

			drawing_canvas: null,
			drawing_painter: null,

			video_loop_timer: null,

			socket: null,
		};
	},
	computed: {},
	watch: {
		/**
		 * Watch Video Element.
		 */
		video() {
			this.clearVideoLoopEvent();
			this.initPainter();
			if (this.video != null) {
				this.onPlayVideo(true, 1000);
			} else {
				return;
			}
		},
	},
	methods: {
		/**
		 * Initialize.
		 * @param {null}
		 * @public
		 */
		initialize: function() {
			this.video_canvas = this.$refs.vod_player;
			this.video_canvas.width = this.width;
			this.video_canvas.height = this.height;
			this.video_painter = this.video_canvas.getContext("2d");

			this.drawing_canvas = this.$refs.drawing;
			this.drawing_canvas.width = this.width;
			this.drawing_canvas.height = this.height;
			this.drawing_painter = this.drawing_canvas.getContext("2d");
		},
		/**
		 * Resize point - Util Method.
		 * @param {target, string} - target and type. type is point or radius or size.
		 * @public
		 * @returns {data} - Resized points data.
		 */
		resizePoint: function(target, type = "point") {
			if (type == "point") {
				var resize = {};
				resize.x = (target.x / 100) * this.width;
				resize.y = (target.y / 100) * this.height;
				return resize;
			} else if (type == "radius") {
				var radius = (target / 100) * this.width;
				return raidus;
			} else if (type == "size") {
				var size = {};
				size.w = (target.w / 100) * this.width;
				size.h = (target.h / 100) * this.height;
				return size;
			}
		},
		/**
		 * Get Label data from Label info List.
		 * @param {string} - Label name.
		 * @public
		 * @returns {string} - color name or hex code.
		 */
		getLabelColor: function(input_label) {
			for (var index = 0; index < this.label_setting.length; ++index) {
				var label = this.label_setting[index];
				if (label.label === input_label) {
					return label.color;
				}
			}
			return "skyblue";
		},
		/**
		 * Draw Objects.
		 * @param {UsedPainter, object, string} - Used Painter and Draw Data Object and Type.
		 * @public
		 */
		drawObjects: function(painter, draw_data, drawing_type) {
			// TYPE : "only_bbox, only_points, both, not_both"
			this.$debug(this.name, "drawObjects", "DRAW DATA:", draw_data);
			var type = drawing_type || this.$t("both_all_see");
			draw_data = draw_data.data;
			if (draw_data && painter) {
				for (var i = 0; i < draw_data.length; ++i) {
					var object = draw_data[i];
					if(object.color) {
						var color = object.color;
					} else {
						var color = this.getLabelColor(object.name);
					}
					if (type === this.$t("only_bbox") || type === this.$t("both_all_see")) {
						var start_point = { x: object.bbox[0] / object.size[0] * this.width,
																y: object.bbox[1] / object.size[1] * this.height };
						var size        = { w: object.bbox[2] / object.size[0] * this.width,
																h: object.bbox[3] / object.size[1] * this.height };
						Painter.drawRect(painter, start_point, size.w, size.h, color, 5, false);
						start_point.y = start_point.y - 10; // text positon.
						Painter.drawText(painter, start_point, object.name + " " + object.score.toFixed(3).toString(), color);
					}
					if (type === this.$t("only_points") || type === this.$t("both_all_see")) {
						if (object.points && object.points.length !== 0) {
							for (var index = 0; index < object.points.length; ++index) {
								var object_point = object.points[index];
								var points = [];
								for (var l = 0; l < object_point.length; ++l) {
									var point = [object_point[l][0][0] / object.size[0] * this.width, object_point[l][0][1] / object.size[1] * this.height];
									points.push(point);
								}
								var text_point = Painter.drawPoly2(painter, points, color, 5, true, false);
								Painter.drawText(painter, text_point, object.name + " " + object.score.toFixed(2).toString(), color);
							}
						}
					}
				}
			}
		},
		/**
		 * Draw Objects.
		 * @param {UsedPainter, list} - Used Painter and Draw object list.
		 * @public
		 */
		drawPolygons: function(painter, objects) {
			for (var object of objects) {
				var points = [];
				var text_start_point = { x: 0, y: 0 };
				var label_info = this.getLabelColor(object.label);
				for (var index = 0; index < object.points.length; ++index) {
					text_start_point.x += object.points[index].x;
					text_start_point.y += object.points[index].y;
					points.push(this.resizePoint(object.points[index]));
				}
				text_start_point.x = text_start_point.x / object.points.length;
				text_start_point.y = text_start_point.y / object.points.length;
				text_start_point = this.resizePoint(text_start_point);
				Painter.drawPoly(painter, points, label_info.color, 5, true, false);
				Painter.drawText(
					painter,
					text_start_point,
					label_info.label,
					label_info.color,
					"center"
				);
			}
		},
		/**
		 * Initialize Painter.
		 * @param {null}
		 * @public
		 */
		initPainter: function () {
			this.video_painter.clearRect(0, 0, this.width, this.height);
			this.drawing_painter.clearRect(0, 0, this.width, this.height);
			if (this.video_loop_timer) {
				this.clearVideoLoopEvent();
			}
		},
		/**
		 * Play Video Event.
		 * @param {bool, number} - loop and fps value.
		 * @public
		 */
		onPlayVideo: function(loop, fps = 30) {
			this.video_painter.drawImage(this.video, 0, 0, this.width, this.height);
			if (loop) {
				this.video_loop_timer = setTimeout(this.onPlayVideo, 1000/fps, loop, fps);
			}
		},
		/**
		 * Draw Object Event in Video.
		 * @param {object} - loop and fps value.
		 * @public
		 */
		onObjectDrawing: function(event) {
			this.drawing_painter.clearRect(0, 0, this.width, this.height);

			if (event) {
				event = JSON.parse(event);
				this.$debug(this.name, "onObjectDrawing", "EVENT:", event.data);
				this.drawObjects(this.drawing_painter, event.data, this.draw_type);
			}
		},
		/**
		 * Close Loop.
		 * @param {null}
		 * @public
		 */
		clearVideoLoopEvent: function() {
			if (this.video_loop_timer) {
				clearTimeout(this.video_loop_timer);
				this.video_loop_timer = null;
			}
		},
	},
	created() {},
	mounted() {
		this.initialize();
	},
	beforeDestroy() {
		this.clearVideoLoopEvent();
	}
};
</script>
<style scoped>
.full-size {
	position: absolute;
	width: 100%;
	height: 100%;
}
canvas {
	position: absolute;
	width: 100%;
	height: 100%;
}
video {
	position: absolute;
	width: 100%;
	height: 100%;
	object-fit: fill;
}

.drawing {
	background-color: rgba(0, 0, 0, 0);
}
</style>