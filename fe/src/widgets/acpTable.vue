<template>
	<v-card class="main">
    <a-timer :timer="timer" :interval="interval" :function="updateTable" ref="table_timer"></a-timer>
		<v-toolbar dense class="toolbar" height="30px">
			<v-spacer />
			<v-btn small icon class="btn" style="width: 30px; height: 30px" @click="openTimerSetting">
				<v-icon size="20">access_time</v-icon>
			</v-btn>
			<v-btn small icon class="btn" style="width: 30px; height: 30px" @click="openDataSetting">
				<v-icon size="20">settings</v-icon>
			</v-btn>
		</v-toolbar>

    <v-card-actions class="datas-label" :style="{'border-bottom': '1px solid ' + border_color}">
      <v-spacer/>
      <span v-if="datas_label != ''" class="data-label">({{$t('unit')}} {{datas_label}})</span>
      <span v-else class="data-label"></span>
    </v-card-actions>

		<div ref="table_parent" class="table_parent" :style="{ 'top': '48px' }">
			<v-data-table 
      :headers="headers" 
      :items="items" 
      class="elevation-3" 
      :no-data-text="$t('no_data_table')"
      hide-actions 
      :hide-headers="headers.length == 0" :style="{'border': '1px solid ' + border_color, 'height': '100%' }">
				<template v-if="hasHeaders2" v-slot:headers="props">
					<tr class="elevation-0">
            <template v-for="(header, index) in props.headers">
              <th v-if="index == 0" 
              :key="index" 
              class="text-xs-center" 
              :style="{'border-right': '1px solid ' + border_color + ' !important'}">{{header}}</th>
              <th v-else :key="index" class="text-xs-center">
                <span :style="{'color': header_font_color, 'font-size': header_font_size, '-webkit-text-stroke': header_font_outline_width + ' ' + header_font_outline_color}">
                  {{header}}
                </span>
              </th>
            </template>
					</tr>
				</template>
        <template v-else v-slot:headers="props">
					<tr>
						<th v-for="(header, index) in props.headers" :key="index" class="text-xs-center">
              <span :style="{'color': header_font_color, 'font-size': header_font_size, '-webkit-text-stroke': header_font_outline_width + ' ' + header_font_outline_color}">
                {{header}}
              </span>
            </th>
					</tr>
				</template>

				<template v-if="hasHeaders2" v-slot:items="props">
          <tr>
            <td class="text-xs-center" :style="{'border-right': '1px solid ' + border_color + ' !important'}">
              <span :style="{'color': header_font_color, 'font-size': header_font_size, '-webkit-text-stroke': header_font_outline_width + ' ' + header_font_outline_color}">
                  {{props.item.header}}
                </span>
            </td> 
            <td class="text-xs-center" v-for="(text, index) in props.item.datas" :key="index">
              {{text}}
            </td>
          </tr>
				</template>
				<template v-else v-slot:items="props">
					<tr>
						<td v-for="(item, index) in props.item" :key="index" class="text-xs-center">{{item}}</td>
					</tr>
				</template>
			</v-data-table>
		</div>

    <transition name="fade">
      <div v-if="open_selector" class="page-dialog">
        <v-card class="page-dialog__content">
          <v-card-title>
            <div>
              <h3 class="headline mb-0">{{$t('data_setting')}}</h3>
            </div>
          </v-card-title>
          <v-card-text style="padding-top: 0 !important; padding-bottom: 0 !important">
            <v-select
              v-model="setting_cache_dataSelect"
              :items="dataList"
              :label="$t('datalist')"
              prepend-icon="library_books"
              :loading="dataListSignal"
              :disabled="dataListSignal"
              solo
              @change="onSelectDataList"
            ></v-select>
            <v-select
              v-if="categoryList"
              v-model="setting_cache_categorySelect"
              :items="categoryList"
              :label="'category'"
              prepend-icon="menu"
              :loading="categoryListSignal"
              :disabled="categoryListSignal"
              solo
            ></v-select>
          </v-card-text>
          <v-card-actions>
            <v-btn @click="onSelectCancel">{{$t('cancel')}}</v-btn>
            <v-spacer />
            <v-btn @click="onSelectApply">{{$t('apply')}}</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </transition>

    <a-timer-setting 
    ref="timer_setting"
    :dialog="timer_setting" 
    :timer_state="timer" 
    :timer_interval="interval"
    @onApply="setTimer($event)" @onClose="closeTimerSetting($event)"/>
	</v-card>
</template>
<script>
import { Observable } from "rxjs";
import aTimer from "@/components/Timer/timer";
import aTimerSetting from "@/components/Dialog/adlgTimerSetting";
import { interval } from 'rxjs/observable/interval';
export default {
	props: {
    /**
     * Resize Trigger. For table dynamic size.
     */
    resizeTrigger: {
      type: Object,
      default: null
    },
    /**
		 * Init Save data from API.
		 */
    component_data: {
      default: null
    }
	},
	components: {
    aTimer,
    aTimerSetting,
  },
	data() {
		return {
      name: "acpTable",
      dataSelect: null,
      dataList: null,
      dataListSignal: false,
      categorySelect: null,
      categoryList: null,
      categoryListSignal: false,
      setting_cache_dataSelect: null,
      setting_cache_categorySelect: null,
      // data from api.
      // headers1: [],
      // headers2: [],
      // datas: [],

      // table style.
      border_color: "rgba(100%, 100%, 100%, 0.12)",
      header_font_color: "yellow",
      header_font_size: "14px",
      header_font_outline_width: "0.0px",
      header_font_outline_color: "black",

      // local data.
      headers: [],
      headers1_label: "",
      headers2_label: "",
      datas_label: "",
      hasHeaders1: false,
      hasHeaders2: false,
      hasDatas2: false,
      items: [],
      table_signal: false,

      // timer data.
      timer: true,
      interval: 3,

      // timer setting.
      timer_setting: false,

      // data selector.
      open_selector: false,
    };
	},
	computed: {
    /**
     * Get Current Theme.
     */
    theme () {
			return this.$vuetify.theme.dark;
    }
  },
  watch: {
    /**
     * Dark and Light theme.
     */
    theme () {
      if (this.theme) {
        this.border_color = "rgba(100%, 100%, 100%, 0.12)";
      } else {
        this.border_color = "grey";
      }
    },
    resizeTrigger () {
      this.onResize();
    }
  },
	methods: {
    /**
		 * Has Data?.
		 * @param {list} - data
		 * @public
     * @returns {bool} - true and false.
		 */
		hasData: function(data) {
      if (!data || data.length === 0) {
        return false;
      } else {
        return true;
      }
			// if (data.length == 0 || data == null || data == undefined) {
			// 	return false;
			// } else {
			// 	return true;
			// }
    },
    /**
		 * insert headers1 data At Two Headers.
		 * @param {list} - Get headers1 from API.
		 * @public
		 */
		headerTwoStyle_header1: function(headers1) {
      this.headers = [];
      if (!this.hasHeaders1) {
        return;
      }
      if (this.hasHeaders2) {
        this.headers.push(" ");
        for (var index = 0; index < headers1.length; ++index) {
          this.headers.push(headers1[index]);
        }
      } else {
        this.headers = headers1.slice();
      }
    },
    /**
		 * insert items data At Two Headers.
		 * @param {listSize, list, list} - headers1List Size, headers2 list, items list.
		 * @public
		 */
		headerTwoStyle_items: function(headers1_length, headers2, datas) {
      if (!this.hasHeaders2) {
        if (!this.hasDatas) {
          return;
        }
        this.items = [];
        this.items = datas.slice();
        return;
      }
      this.items = [];
      for (var index = 0; index < headers2.length; ++index) {
        var temp_item = {};
        temp_item.header = headers2[index];
        if (!this.hasDatas) {
          temp_item.datas = [];
          for (var idx = 0; idx < headers1_length; ++idx) {
            temp_item.datas.push("");
          }
        } else {
          temp_item.datas = datas[index];
        }
        this.items.push(temp_item);
      }
    },
    /**
     * Convert response data to Table data.
     * @param {object} - response data.
     * @public
     */
    convertTableData: function (response) {
      this.hasHeaders1 = this.hasData(response.header1);
      if (!this.hasHeaders1) {
        response.header1 = [];
      }
      this.hasHeaders2 = this.hasData(response.header2);
      if (!this.hasHeaders2) {
        response.header2 = [];
      }
      this.hasDatas = this.hasData(response.data);
      this.headers1_label = response['header1-label'];
      this.headers2_label = response['header2-label'];
      this.datas_label    = response['data-label'];
      this.headerTwoStyle_header1(response.header1);
      this.headerTwoStyle_items(response.header1.length, response.header2, response.data);

      this.$debug(this.name, "convertTableData", "Headers:", this.headers);
      this.$debug(this.name, "convertTableData", "Items:", this.itmes);
    },
    /**
     * Update Table, Send signal to API.
     * @param {null}
     * @public
     */
    updateTable: function () {
      if (!this.table_signal) {
        this.table_signal = true;
      }
    },
    /**
     * Open Timer Setting Dialog.
     * @param {null}
     * @public
     */
    openTimerSetting: function () {
      this.timer_setting = true;
    },
    /**
     * Open Table Setting Dialog.
     * @param {null}
     * @public
     */
    openDataSetting: function () {
      this.open_selector = true;
      setTimeout(()=> {this.dataListSignal = true}, 500);
      this.setting_cache_dataSelect = this.dataSelect;
      this.setting_cache_categorySelect = this.categorySelect;
    },
    /**
     * Close Timer Setting Dialog.
     * @param {null}
     * @public
     */
    closeTimerSetting: function (event) {
      this.timer_setting = false;
    },
    /**
     * Set Interval of timer.
     * @param {object} - Timer Setting Values. 
     * @public
     */
    setTimer: function (event) {
      this.$debug(this.name, "setTimer", "Interval:", event.interval, "Status:", event.state);
      this.interval = Number(event.interval);
      this.timer = event.state;
    },
    /**
     * Close Data Setting Dialog.
     * @param {object} - Timer Setting Values. 
     * @public
     */
    closeDataSelector: function (event) {
      this.open_selector = event;
    },
    /**
     * Resize Event.
     * @param {null}
     * @public
     */
    onResize: function () {
      var parent = this.$refs.table_parent;
      var table = parent.firstChild.firstChild.firstChild;
      if (parent.clientWidth < table.clientWidth) {
        parent.firstChild.firstChild.style.width = String(table.clientWidth) + "px";
      } else {
        parent.firstChild.firstChild.style.width = "100%";
      }
      if (parent.clientHeight < table.clientHeight) {
        parent.firstChild.firstChild.style.height = String(table.clientHeight) + "px";
      } else {
        parent.firstChild.firstChild.style.height = "100%";
      }
    },
    /**
     * Select Data list event.
     * @param {null}
     * @public
     */
    onSelectDataList: function () {
      this.categoryListSignal = true;
    },
    /**
     * Apply event of Data Setting Dialog.
     * @param {null}
     * @public
     */
    onSelectApply: function () {
      this.dataSelect = this.setting_cache_dataSelect;
      this.categorySelect = this.setting_cache_categorySelect;
      this.open_selector = false;
    },
    /**
     * Cancel event of Data Setting Dialog.
     * @param {null}
     * @public
     */
    onSelectCancel: function () {
      this.open_selector = false;
    },
    /**
		 * Trans Save Component Data To API.
		 * @param {null}
		 * @public
		 */
    saveApi: function () {
			var component_data = {};
      component_data.timer = this.timer;
      component_data.interval = this.interval;
      component_data.dataSelect = this.dataSelect;
      component_data.categorySelect = this.categorySelect;
			this.$emit("component_data", component_data);
    },
    /**
		 * Load Component Data From API.
		 * @param {null}
		 * @public
		 */
    loadDataFromAPI: function () {
      if (this.component_data) {
        var copy_data = this.$util.cloneObject(this.component_data);
        for (var key in copy_data) {
          switch (key) {
            case "timer": {
              this.timer = copy_data[key];
              break;
            }
            case "interval": {
              this.interval = copy_data[key];
              break;
            }
            case "dataSelect": {
              this.dataSelect = copy_data[key];
              break;
            }
            case "categorySelect": {
              this.categorySelect = copy_data[key];
              break;
            }
            default: {
              this.$warn(this.name, "loadDataFromAPI", "The key(", key, ") is not used.");
              break;
            }
          }
        }
      }
    }
	},
	created() {},
  mounted() {
    this.onResize();
    this.loadDataFromAPI();
    if (this.timer) {
      setTimeout(this.$refs.table_timer.onStart(), 500);
    }
  },
  beforeDestroy() {
    this.saveApi();
  },
  subscriptions() {
		const $table_signal = this.$watchAsObservable("table_signal", {immediate: true})
			.pluck("newValue")
      .filter(table_signal => table_signal == true) // if signal is true.
    const $dataListSignal = this.$watchAsObservable("dataListSignal", {immediate: true})
      .pluck("newValue")
      .filter(dataListSignal => dataListSignal == true)
    const $categoryListSignal = this.$watchAsObservable("categoryListSignal", {immediate: true})
      .pluck("newValue")
      .filter(categoryListSignal => categoryListSignal == true)
		return {
      table_result: Observable.combineLatest($table_signal, table_signal => ({ table_signal }))
        .flatMap(({ table_signal }) =>
        this.$api.getTableData(this.$store.getters["user/getAccessToken"], this.dataSelect, this.categorySelect)
					.do(res => {
            this.$debug(this.name, "subscriptions::table_result", "Response:", res);
            if (res) {
              this.convertTableData(res);
            }
            this.onResize();
					})
					.catch(err => {
            this.$error(this.name, "subscriptions::table_result", err);
						return Observable.of(null);
					})
					.do(() => {
						this.table_signal = false;
					})
      ),
      datalist_result: Observable.combineLatest($dataListSignal, dataListSignal => ({ dataListSignal }))
        .flatMap(({ dataListSignal }) =>
        this.$api.getTableDataList(this.$store.getters["user/getAccessToken"])
					.do(res => {
            this.$debug(this.name, "subscriptions::datalist_result", "Response:", res);
            this.dataList = res.datalist;
					})
					.catch(err => {
            this.$error(this.name, "subscriptions::datalist_result", err);
						return Observable.of(null);
					})
					.do(() => {
						this.dataListSignal = false;
					})
      ),
      categorylist_result: Observable.combineLatest($categoryListSignal, categoryListSignal => ({ categoryListSignal }))
        .flatMap(({ categoryListSignal }) =>
        this.$api.getTableCategoryList(this.$store.getters["user/getAccessToken"], this.setting_cache_dataSelect)
					.do(res => {
            this.$debug(this.name, "subscriptions::categorylist_result", "Response:", res);
            this.categoryList = res.categories;
					})
					.catch(err => {
						this.$error(this.name, "subscriptions::categorylist_result", err);
						return Observable.of(null);
					})
					.do(() => {
						this.categoryListSignal = false;
					})
			)
		};
	}
};
</script>
<style scoped>
.border {
	border: 1px solid yellowgreen;
}
.main {
	width: 100%;
	height: 100%;
}
.v-toolbar:hover {
  cursor: move;
}
.toolbar {
  margin-top: 0;
  margin-bottom: 0;
}
.progress {
  margin-top: 0;
  margin-bottom: 0;
}
/* .v-card__actions { */
.datas-label {
  margin: 0;
  padding: 0;
  height: 18px;
}
.data-label {
  font-size: 12px;
}
.table_parent {
  position: absolute;
  width: 100%;
	height: calc(100% - 48px);
	overflow-y: auto;
}
.mytable {
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: auto;
}
.table_parent >>> .v-table__overflow {
  overflow-x: hidden !important;
  /* height: 100%; */
}
.table_parent >>> table {
  height: 100%;
}

.page-dialog {
	position: absolute;
	display: flex;
	flex-wrap: wrap;
	width: 100%;
	height: calc(100% - 30px);
	/* padding: 15px 15px 15px 15px; */
	background-color: rgba(25,25,25,0.7);
	overflow: auto;
	justify-content: center;
	align-content: center;
}
.page-dialog__content {
	width: auto;
	max-width: 95%;
	max-height: 100%;
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

/* thead th:nth-child(1) {
  border-right: 1px solid rgba(100%, 100%, 100%, 0.12) !important;
}
thead th {
  border-bottom: 1px solid rgba(100%, 100%, 100%, 0.12) !important 
}
.table_parent >>> tbody tr td:nth-child(1) {
  border-right: 1px solid rgba(100%, 100%, 100%, 0.12) !important;
} */
/* span {
  border: 1px solid red;
  color: yellow;
  -webkit-text-stroke: 0.5px black;
  font-size: 18px
} */
</style>