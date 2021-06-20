<template>
  <v-navigation-drawer
    clipped
    app
    stateless
    touchless
    :value="navi_show"
    :width="navi_width"
    class="answer-navigation"
    :style="this.$backgroundColor()"
  >
    <a-list
      ref="navigationList"
      :header="projectInfo"
      :lists="navi_list"
      :i18nMain="true"
      :i18nExpand="true"
      @mainClick="onClickMainItem($event)"
      @subClick="onClickSubItem($event)"
      @mainGroupClick="onClickGroupItem($event)"
      @expandClick="onClickExpandItem($event)"
    ></a-list>
  </v-navigation-drawer>
</template>

<script>
import { Observable } from "rxjs";

/**
 * Asnwer Main Navigation Drawer.
 * @author hadoo 2019-06-24
 */
export default {
  name: "adrNavigation",
  props: {},
  data() {
    return {};
  },
  methods: {
    /**
     * Click Project name event. Go to Project Main page.
     * @param {null}
     * @public
     */
    gotoProjectMain: function() {
      // 현재는 네비게이션의 레이아웃을 다시 로드한다.
      // 다시 로드할 때 첫번 째 레이아웃으로 이동할 지 없을 경우에는 가이드 페이지로 이동할 지 정하기 때문에 사용.
      this.$store.commit("signal/setLayoutMainSignal", { bool: true });
    },

    /**
     * All deselected event of answer list.
     * @public
     */
    listAllDeselected: function() {
      this.$refs.navigationList.allDeselected();
    },

    /**
     * This is MainMenu Click Event.
     * @param {object} - Selected Main Menu item.
     * @public
     */
    onClickMainItem: function(list) {
      // if have not sub item, this go to page.
      this.$store.commit("project/setSelectLayout", { layoutName: null });
      this.$router
        .push(this.$page.project + "/" + list.title.toLowerCase() + "/")
        .catch(() => {});
    },

    /**
     * This is GroupMenu Click Event.
     * @public
     * @param {object} - Select Group menu item.
     */
    onClickGroupItem: function($event) {
      if (!$event.active) {
        return;
      }
      if ($event.title === "layout") {
        this.$store.commit("signal/setLayoutMainSignal", { bool: true });
      }
    },

    /**
     * This is SubMenu Click Event.
     * @param {object} - Selected SubMenu item.
     * @public
     */
    onClickSubItem: function($event) {
      this.$store.commit("project/setSelectLayout", {
        layoutName: $event.subItem.name,
      });
      this.$router
        .replace(
          this.$page.project +
            "/" +
            $event.list.title.toLowerCase() +
            "/" +
            $event.subItem.name
        )
        .catch(() => {});
    },

    /**
     * This is Expand Menu Click Event.
     * @public
     * @param {object} - Selected expand menu item.
     */
    onClickExpandItem: function($event) {
      var mainItem = $event.list;
      var expandItem = $event.expandItem;
      if (mainItem.title === "layout") {
        if (expandItem.title) {
          if (expandItem.title === "add_layout") {
            this.$store.commit("drawer/setOpenAddLayout", { bool: true });
          }
        } else if (expandItem.name) {
          if (expandItem.name === "add_layout") {
            this.$store.commit("drawer/setOpenAddLayout", { bool: true });
          }
        }
      }
    },
  },
  computed: {
    navi_show() {
      return this.$store.getters["drawer/getNaviShow"];
    },
    navi_width() {
      return this.$store.getters["drawer/getNaviWidth"];
    },
    projectInfo() {
      var info = {
        title: this.$store.getters["project/getSelectProject"],
        icon: undefined,
      };
      return info;
    },
    navi_list() {
      return this.$store.getters["project/getViewMenuList"];
    },
    layout_main_signal() {
      return this.$store.getters["signal/getLayoutMainSignal"];
    },
  },
  watch: {
    layout_main_signal() {
      if (this.layout_main_signal) {
        this.$store.commit("etc/setLoadingLiner", { bool: true });
      } else {
        this.$store.commit("etc/setLoadingLiner", { bool: false });
      }
    },
  },
  mounted() {},
  subscriptions() {
    const $layout_main_signal = this.$watchAsObservable("layout_main_signal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((layout_main_signal) => layout_main_signal == true); // if signal is true.
    // .debounceTime(1000);
    return {
      main_result: Observable.combineLatest(
        $layout_main_signal,
        (layout_main_signal) => ({ layout_main_signal })
      ).flatMap(({ layout_main_signal }) =>
        this.$api
          .getLayouts(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"]
          )
          .do((res) => {
            this.$debug(
              this.$options.name,
              "subscriptions::getLayouts",
              "Response:",
              res
            );
            if (!res.layouts) {
              this.$error(
                this.$options.name,
                "subscriptions::getLayouts",
                "Response is wrong:",
                res
              );
              // this.$router.push(this.$page.projects);
              return;
            }
            this.$store.commit("project/setLayouts", { layouts: res.layouts });
            this.$nextTick().then(() => {
              if (res.layouts.length !== 0) {
                this.$debug(
                  this.$options.name,
                  "subscriptions::getLayouts",
                  "check store getSelectLayout:",
                  this.$store.getters["project/getSelectLayout"]
                );
                if (this.$store.getters["project/getSelectLayout"]) {
                  var selectIndex = -1;
                  for (var i = 0; i < this.navi_list.length; ++i) {
                    if (this.navi_list[i].submenu) {
                      for (
                        var j = 0;
                        j < this.navi_list[i].submenu.length;
                        ++j
                      ) {
                        if (
                          this.navi_list[i].submenu[j].name ===
                          this.$store.getters["project/getSelectLayout"]
                        ) {
                          this.$refs.navigationList.onClickSubList(
                            this.navi_list[i].submenu[j],
                            this.navi_list[i]
                          );
                          selectIndex = j;
                        }
                      }
                    }
                  }
                  if (selectIndex < 0) {
                    this.$debug(
                      this.$options.name,
                      "subcriptions::getLayouts",
                      "Not matched pre select layout and first layout."
                    );
                    this.$store.commit("project/setSelectLayout", {
                      layoutName: res.layouts[0],
                    });
                    if (this.navi_list[0].submenu) {
                      this.$refs.navigationList.onClickSubList(
                        this.navi_list[0].submenu[0],
                        this.navi_list[0]
                      );
                    }
                  }
                } else {
                  this.$store.commit("project/setSelectLayout", {
                    layoutName: res.layouts[0],
                  });
                  if (this.navi_list[0].submenu) {
                    this.$refs.navigationList.onClickSubList(
                      this.navi_list[0].submenu[0],
                      this.navi_list[0]
                    );
                  }
                }
              } else {
                this.$router.replace(this.$page.project + "/" + "guide_layout");
              }
            });
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::getLayouts", err);
            return Observable.of(null);
          })
          .do(() => {
            this.$store.commit("signal/setLayoutMainSignal", { bool: false });
          })
      ),
    };
  },
};
</script>

<style scoped>
.answer-navigation {
  z-index: 191;
}
</style>
