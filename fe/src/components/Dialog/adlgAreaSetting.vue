<template>
  <v-dialog
    v-model="dialog"
    scrollable 
    persistent :overlay="false"
    max-width="500px"
    transition="dialog-transition"
		:dark="this.$vuetify.theme.dark"
  >
		<v-card id="card-main">
      <div id="edit-zone">
				<vod-area-drawer id="area_zone" ref="area_zone" :eidt="true"></vod-area-drawer>
      </div>
      <v-toolbar height="40">
        <v-btn small @click="onCancel">cancel</v-btn>
        <v-spacer></v-spacer>
        <v-btn small :loading="send_signal" :disabled="send_signal" @click="onOk">ok</v-btn>
      </v-toolbar>
		</v-card>
  </v-dialog>
</template>

<script>
/**
 * Roi setting dialog. (Unused instead of Lambdawidget)
 * @author hadoo
 */
import { Observable } from "rxjs";
import VodAreaDrawer from "@/widgets/acpVodPlayer.vue";
export default {
	name: "adlgAreaSetting",
  props:{
		/**
		 * Dialog show and hide.
		 */
    dialog: {
      type: Boolean,
      default: false,
		},
		/**
		 * Selected lambda id.
		 */
    lambda_id: {
      type: Number,
      default: 0,
		},
		
		/**
		 * Selected property name.
		 */
    prop_name: {
      type: String,
      default: "",
		},
		
		/**
		 * Presave data for preview.
		 */
    presave_data: {
      type: Object,
      default () {
        return {};
      }
		}
  },
  components:{
		VodAreaDrawer
  },
  data(){
    return {
      canvas: null,
      send_data: null,
      send_signal: false,
    }
  },
  computed:{
  },
  watch: {
    // presave_data: {
    //   if (this.presave_data.length !== 0) {
    //     console.log("PreSave Data: ", this.presave_data);
    //     // this.$refs.area_zone.setEventAreaToPainter(this.presave_data);
    //   }
		// }
		dialog() {
			if (this.dialog) {
				if (this.presave_data) {
					this.$nextTick(() => {
						this.$refs.area_zone.setEventAreaToPainter(this.presave_data);
					})
				}
			}
		}
  },
  methods:{
		/**
		 * Cancel event.
		 * @public
		 */
    onCancel: function () {
			this.$refs.area_zone.destroy();
			/**
			 * For dialog close.
			 * @property {boolean} - cancel value false.
			 */
      this.$emit("onCancel", false);
		},
		
		/**
		 * Send edit data to API.
		 * @public
		 */
    onOk: function () {
      this.send_data = {};
			this.send_data.id = this.lambda_id;
			var areazone = this.$refs.area_zone;
			var areas = areazone.getAreaData();
			var event_area = [];
			event_area.push(areazone.convertLinesForAPI(areas.lines));
			event_area.push(areazone.convertRectsForAPI(areas.rects));
			event_area.push(areazone.convertPolysForAPI(areas.polys));
      event_area.push(areazone.convertArcsForAPI(areas.arcs));
			this.send_data.event_area = event_area;
			this.$debug(this.$options.name, "onOk", "SendData:", this.send_data);
      this.send_signal = true;
      // this.$emit("onOk", true);
		},

		/**
		 * Convert line data for API.
		 * @public
		 * @param {array} - lines data.
		 * @return {object} - converting data.
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
		 * Convert rect data for API.
		 * @public
		 * @param {array} - rects data.
		 * @return {object} - converting data.
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
		 * Convert polygons data for API.
		 * @public
		 * @param {array} - polygons data.
		 * @return {object} - converting data.
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
		 * Convert Arc(circle) data for API.
		 * @public
		 * @param {array} - circles data.
		 * @return {object} - converting data.
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
  },
  created(){
  },
  mounted(){
  },
  subscriptions() {
		const $send_signal = this.$watchAsObservable("send_signal", {
			immediate: true
		})
			.pluck("newValue")
			.filter(send_signal => send_signal == true) // if signal is true.
			.debounceTime(1000); // delay 1s.
		return {
			main_result: Observable.combineLatest($send_signal, send_signal => ({
				send_signal
			})).flatMap(({ send_signal }) =>
				// LOCAL_API.getLambdaData()
				this.$api.setEventRoi(this.$store.getters["user/getAccessToken"], this.lambda_id, this.prop_name, this.send_data)
					.do(res => {
            // console.log("[adlgAreaSetting::subscriptions] Response", res);
            if (res.status === "ERROR") {
							this.$error(this.$options.name, "subscriptions::setEventRoi", "RESPONSE-ERROR:", res.detail);
              return Observable.of(null);
            } else {
              this.$refs.area_zone.clearAllToPainter();
							this.$refs.area_zone.destroy();
							/**
							 * Edit area data send to api success.
							 * @property {boolean} - success value true.
							 */
              this.$emit("onOk", true);
            }
					})
					.catch(err => {
						this.$error(this.$options.name, "subscriptions::setEventRoi", "NETWORK-ERROR:", err);
						return Observable.of(null);
					})
					.do(() => {
						this.send_signal = false;
					})
			)
		};
	}
}
</script>

<style scoped>
#card-main {
  width: 500px;
  max-width: 500px;
  min-width: 250px;
  height: 400px;
  max-height: 400px;
  min-height: 200px;
}
#edit-zone {
  width: 100%;
  height: calc(100% - 40px);
}

</style>