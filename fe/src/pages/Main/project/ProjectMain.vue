<template>
  <v-container class="project-main">
    <adr-navigation>
    </adr-navigation>

    <adr-components>
    </adr-components>

    <adlg-add-layout>
    </adlg-add-layout>

    <router-view>
    </router-view>
  </v-container>
</template>

<script>
import adrNavigation from '@/components/Drawer/adrNavigation.vue';
import adrComponents from '@/components/Drawer/adrComponents.vue';
import adlgAddLayout from '@/components/Dialog/adlgAddLayout.vue';
import { Observable } from "rxjs";

export default {
  name: "ProjectPage",
  components: {
    adrNavigation,
    adrComponents,
    adlgAddLayout,
  },
  data() {
    return {
      project_signal: false,
    };
  },
  methods: {},
  computed: {},
  watch: {
    project_signal() {
      if (this.project_signal) {
        this.$store.commit("etc/setLoadingLiner", { bool: true });
      } else {
        this.$store.commit("etc/setLoadingLiner", { bool: false });
      }
    },
  },
  mounted() {
    this.project_signal = true;
    this.$store.commit("drawer/setNaviShow", { bool: true });
  },
  beforeDestroy() {
    this.$store.commit("drawer/setNaviShow", { bool: false });
    this.$store.commit("project/setViewNaviList", { menus: null });
  },
  subscriptions() {
    const $project_signal = this.$watchAsObservable("project_signal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((project_signal) => project_signal == true); // if signal is true.
    // .debounceTime(5000)
    return {
      result: Observable.combineLatest($project_signal, (project_signal) => ({
        project_signal,
      })).flatMap(({ project_signal }) =>
        this.$api
          .getProject(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"]
          )
          .do((res) => {
            // console.log("[ProjectMain::subscriptions] ", res);
            this.$debug(
              this.$options.name,
              "ProjectMain::getProject",
              "RESPONSE:",
              res
            );
            if (!res.name) {
              this.$error(
                this.$options.name,
                "ProjectMain::getProject",
                "Response is wrong:",
                res
              );
              return;
            }
            this.$store.commit("project/setSelectProject", { name: res.name });
            this.$store.commit("project/setViewNaviList", { menus: res.menus });
            this.$store.commit("signal/setLayoutMainSignal", { bool: true });
          })
          .catch((err) => {
            this.$error(
              this.$options.name,
              "[ProjectMain::subscriptions] ",
              err
            );
            if (err.message === "Network Error") {
              this.$error(
                this.$options.name,
                "ProjectMain::getProject",
                "Network Error. Goto LoginPage. And Logout."
              );
              this.$store.commit("user/logout");
              this.$router.push("/");
            }
            return Observable.of(null);
          })
          .do(() => {
            this.project_signal = false;
          })
      ),
    };
  },
};
</script>

<style>
.project-main {
  height: 100%;
}
</style>
