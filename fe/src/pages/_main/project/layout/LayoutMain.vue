<template>
  <div class="layout-main">
    <div class="dashboard-zone">
      <adb-dashboard :active="active"></adb-dashboard>
    </div>
  </div>
</template>

<script>
import { Observable, ObjectUnsubscribedError } from "rxjs";

import adbDashboard from "@/components/Dashboard/adbDashboard";

export default {
  name: "LayoutMainPage",
  components: {
    adbDashboard,
  },
  props: {},

  data() {
    return {
      layout_signal: true,
      name: "",
      panels: Object,
    };
  },
  methods: {
    getDashboardDataFromStore: function() {
      return this.$store.getters["dashboard/getDashInfos"];
    },
  },
  computed: {
    active() {
      return this.$store.getters["dashboard/getDashActive"];
    },
    submenu_title() {
      return this.$store.getters["project/getSelectLayout"];
    },
  },
  watch: {
    layout_signal() {
      if (this.layout_signal) {
        this.$store.commit("etc/setLoadingLiner", { bool: true });
      } else {
        this.$store.commit("etc/setLoadingLiner", { bool: false });
      }
    },
    submenu_title() {
      this.layout_signal = true;
    },
  },
  beforeDestroy() {
    this.$store.commit("drawer/setCompoOpen", { bool: false });
  },
  subscriptions() {
    const $layout_signal = this.$watchAsObservable("layout_signal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((layout_signal) => layout_signal == true); // if signal is true.
    return {
      main_result: Observable.combineLatest(
        $layout_signal,
        (layout_signal) => ({
          layout_signal,
        })
      ).flatMap(({ layout_signal }) =>
        this.$api
          .getLayout(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.$store.getters["project/getSelectLayout"]
          )
          .do((res) => {
            // console.log("[LayoutMain::subcriptions] ", res);
            this.name = res.name;
            // this.panels = JSON.parse(res.panels);
            this.panels = this.$util.dashboard_sToj(res.panels);
            this.$store.commit("dashboard/setPanels", { panels: this.panels });
          })
          .catch((err) => {
            console.log("[LayoutMain::subcriptions] ", err);
            return Observable.of(null);
          })
          .do(() => {
            this.layout_signal = false;
          })
      ),
    };
  },
};
</script>

<style>
.layout-main {
  height: 100% !important;
  /* padding: 25px 25px 25px 25px !important; */
  /* padding: 10px 10px 10px 10px !important; */
  /* border: 1px solid royalblue !important; */
}
.editor-zone {
  height: 1% !important;
  /* border: 1px solid greenyellow !important; */
  /* width: 100%;
	height: 2%; */
}
.edit-btn {
  margin-right: -13px;
  margin-top: 22px;
}
.dashboard-zone {
  height: 100% !important;
  /* border: 1px solid yellow !important; */
}
</style>
