<template>
	<v-splitpanes class="default-theme" style="position: absolute; padding: 10px;" @resized="refresh">
		<v-pane :size="75" :min-size="25" style="background-color: transparent;">
			<div style="width: 100%; height: 100%;">
				<visual-graph 
					ref="graph" 
					@openDeleteCheck="openDeleteCheck"
					@selectedLambda="selectedLambda($event)" 
					@deselectedLambda="deselectedLambda($event)"
					@selectedTask="selectedTask($event)"
					@deselectedTask="deselectedTask($event)">
				</visual-graph>
			</div>
		</v-pane>
		<v-pane :size="20" style="background-color: transparent;" :min-size="10">
			<div style="width: 100%; height: 100%;">
				<detail-setting ref="detail_setting" 
					@saveSetting="saveSetting($event)"
					@deleteLambdaNTask="deleteLambdaNTask($event)">
				</detail-setting>
			</div>
		</v-pane>
	</v-splitpanes>
</template>
<script>
import "@/components/VisualGraph/litegraph.css";
import VisualGraph from "@/components/VisualGraph/vgCanvas.vue";
import DetailSetting from "@/components/VisualGraph/vgDetailSetting.vue";

// import * as API from "@/components/Test/javascript/test.js";
// import * as API from "@/services/api.js";

export default {
	props: {},

	components: {
		VisualGraph,
		DetailSetting,
	},

	data() {
		return {
		};
	},

	computed: {
	},

	watch: {
	},

	methods: {
		refresh: function () {
			var drawData = this.$util.cloneObject(this.$refs.graph.graph_controller.serialize());
			console.log("DATA", drawData);
			// if (this.$refs.graph.graph_controller) {
			// 	this.$refs.graph.graph_controller = null;
			// }
			// if (this.$refs.graph.graph_canvas) {
			// 	this.$refs.graph.graph_canvas = null;
			// }
			// this.$refs.graph.initialize();
			// this.$refs.graph.graph_controller.configure(drawData);
			// this.$refs.graph.graph_controller.change();
		},
		initialize: function() {
			/** empty */
		},

		/**
		 * Open Delete Check Dialog from ContextMenu.
		 * @public
		 * @param {null}
		 */
		openDeleteCheck: function () {
			if (this.$refs.detail_setting) {
				this.$refs.detail_setting.onDelete();
			}
		},

		/**
		 * Send lambda's data to the detail setting window when a lambda`s selected event occurs.
		 * @public
		 * @param {lambdaData} - Lambda`s Data.
		 */
		selectedLambda: function(lambdaData) {
			if (this.$refs.detail_setting) {
				this.$refs.detail_setting.loadData(lambdaData);
			} else {
				console.error("[vgMain::selectedLambda] [ERROR] Ref: detail_setting is null.");
			}
		},

		/**
		 * Initialize the detail setting window when a lambda`s deselected event occurs.
		 * @public
		 * @param {null}
		 */
		deselectedLambda: function() {
			if (this.$refs.detail_setting) {
				this.$refs.detail_setting.initialize();
			} else {
				console.error("[vgMain::deselectedLambda] [ERROR] Ref: detail_setting is null.");
			}
		},

		/**
		 * Send task's data to the detail setting window when a task`s selected event occurs.
		 * @public
		 * @param {taskData} - task`s Data.
		 */
		selectedTask: function(taskData) {
			if (this.$refs.detail_setting) {
				this.$refs.detail_setting.loadData(taskData);
			} else {
				console.error("[vgMain::selectedTask] [ERROR] Ref: detail_setting is null.");
			}
		},

		/**
		 * Initialize the detail setting window when a task`s deselected event occurs.
		 * @public
		 * @param {null}
		 */
		deselectedTask: function() {
			if (this.$refs.detail_setting) {
				this.$refs.detail_setting.initialize();
			} else {
				console.error("[vgMain::deselectedTask] [ERROR] Ref: detail_setting is null.");
			}
		},

		/**
		 * Send modified task's data to the graph canvas window when a task`s data save event occurs.
		 * @public
		 * @param {result} - modified lambda or task data.
		 */
		saveSetting: function(result) {
			if (this.$refs.graph) {
				this.$refs.graph.saveSetting(result);
			} else {
				console.error("[vgMain::saveSetting] [ERROR] Ref: graph is null.");
			}
		},

		/**
		 * Send Lambda or Task delete event to graph canvas when a lambda or task delete event occurs.
		 * @public
		 * @param {object} - lambda or task.
		 */
		deleteLambdaNTask: function (object) {
			if (this.$refs.graph) {
				this.$refs.graph.deleteLambdaNTask(object);
			} else {
				console.error("[vgMain::saveSetting] [ERROR] Ref: graph is null.");
			}
		},

		/**
		 * Resize Event - Unused.
		 * @public
		 * @param {event} - Unused.
		 */
		onResize: function(event) {
			// if (this.window_resize) {
			// 	var set_canvas = this.$refs.mycanvas;
			// 	set_canvas.width = set_canvas.clientWidth;
			// 	set_canvas.height = set_canvas.clientHeight;
			// 	this.canvas.setCanvas(set_canvas);
			// 	this.graph.change();
			// }
		},
	},

	created() {
	},

	mounted() {
	},
};
</script>

<style scoped>
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