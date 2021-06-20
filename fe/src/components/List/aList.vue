<template>
  <div class="answer-list">
    <v-toolbar v-if="header" dense class="transparent elevation-1">
      <v-avatar class="header-avatar" size="35" style="margin-left: -5px;">
        <v-icon v-if="header.icon" v-text="header.icon" small></v-icon>
        <span v-else class="header-avatar-text">
          {{ header.title ? header.title.substring(0, 1).toUpperCase() : "" }}
        </span>
      </v-avatar>
      <v-toolbar-title class="text-center" style="width: 100%;">
        <strong class="header-text">
          {{ useI18n(header.title, i18nHeader) }}
        </strong>
      </v-toolbar-title>
    </v-toolbar>
    <v-list class="list-style">
      <template v-for="list in lists">
        <v-list-group
          v-if="list.submenu"
          :key="list.title || list.name"
          :ref="list.title ? 'main_' + list.title : 'main_' + list.name"
          :value="list.active"
          :active-class="null"
          @click="onClickMainGroupList(list)"
          :prepend-icon="list.icon"
        >
          <v-list-item-content slot="activator">
            <div class="fit-font">
              {{
                list.title
                  ? useI18n(list.title, i18nMain)
                  : useI18n(list.name, i18nMain)
              }}
            </div>
          </v-list-item-content>
          <v-list-item
            v-for="subItem in list.submenu"
            ripple
            :key="subItem.title || subItem.name"
            @click="onClickSubList(subItem, list)"
            :ref="
              subItem.title ? 'sub_' + subItem.title : 'sub_' + subItem.name
            "
          >
            <v-list-item-action>
              <v-icon small>{{ subItem.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-subtitle>
              {{
                subItem.title
                  ? useI18n(subItem.title, subItem.i18n, subItem.upper)
                  : useI18n(subItem.name, subItem.i18n, subItem.upper)
              }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-list-item
            v-for="expand in list.expands"
            ripple
            :key="expand.title || expand.name"
            @click="onClickExpandList(expand, list)"
            :ref="
              expand.title ? 'expand_' + expand.title : 'expand_' + expand.name
            "
          >
            <v-list-item-action>
              <v-icon small>{{ expand.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-subtitle>{{
              expand.title
                ? useI18n(expand.title, i18nExpand)
                : useI18n(expand.name, i18nExpand)
            }}</v-list-item-subtitle>
          </v-list-item>
        </v-list-group>
        <v-list-item
          v-else
          ripple
          :key="list.title || list.name"
          :ref="list.title ? 'main_' + list.title : 'main_' + list.name"
          @click="onClickMainList(list)"
          :prepend-icon="list.icon"
        >
          <v-list-item-action>
            <v-icon :size="25">{{ list.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <div class="fit-font">
              {{
                list.title
                  ? useI18n(list.title, i18nMain)
                  : useI18n(list.name, i18nMain)
              }}
            </div>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </div>
</template>

<script>
export default {
  name: "AnswerList",
  version: "1.0.0",
  props: {
    // 부모로부터 데이터를 받는 부분. 생성자의 Args와 비슷.
    /**
     * 'header' is Title of List.
     * ex) { title: "", icon: "" or undefined }
     */
    header: {
      type: Object,
      default: undefined,
      // default() { return { title: 'please insert header name', icon: undefined}; }
    },
    /**
     * 'lists' is item of list.
     */
    lists: {
      type: Array,
      // eslint-disable-next-line vue/require-valid-default-prop
      default: [],
      required: false,
    },
    /**
     * on/off i18n about header text.
     */
    i18nHeader: {
      type: Boolean,
      default: false,
      required: false,
    },
    /**
     * on/off i18n about main item of list.
     */
    i18nMain: {
      type: Boolean,
      default: false,
      required: false,
    },
    /**
     * on/off i18n about sub item of main item.
     */
    i18nSub: {
      type: Boolean,
      default: false,
      required: false,
    },
    /**
     * on/off i18n about expand item of main item.
     */
    i18nExpand: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  components: {},
  data() {
    return {
      DARK: {
        DESELECTED: "rgba(203, 203, 203, 0)",
        SELECTED: "rgba(203, 203, 203, 0.5)",
      },
      LIGHT: {
        DESELECTED: "rgba(5, 5, 5, 0)",
        SELECTED: "rgba(5, 5, 5, 0.5)",
      },
      selfLists: [], // empty object.
    };
  },

  computed: {
    DESELECTED() {
      if (this.$vuetify.theme.dark) {
        return this.DARK.DESELECTED;
      } else {
        return this.LIGHT.DESELECTED;
      }
    },
    SELECTED() {
      if (this.$vuetify.theme.dark) {
        return this.DARK.SELECTED;
      } else {
        return this.LIGHT.SELECTED;
      }
    },
  },
  watch: {},
  methods: {
    /**
     * Initialize.
     * @public
     * @param {null}
     */
    initialize: function() {
      /** Empty */
    },

    /**
     * Toggle on off i18n.
     * @public
     * @param {string} - text to use.
     * @param {boolean} - toggle on/off.
     */
    useI18n: function(text, isUse, upper) {
      var isUpper = true;
      var use = isUse || false;
      if (!upper) {
        isUpper = false;
      }
      if (use) {
        if (isUpper) {
          return this.$t(text).toUpperCase();
        } else {
          return this.$t(text);
        }
      } else {
        if (isUpper) {
          return text.toUpperCase();
        } else {
          return text;
        }
      }
    },

    /**
     * Select list`s item. Change Selected Color.
     * @public
     * @param {string} - vue ref`s name.
     */
    selectedList: function(refName) {
      this.allDeselected();
      if (this.$refs[refName][0]) {
        this.$refs[refName][0].$el.style.backgroundColor = this.SELECTED;
        this.$debug(
          this.$options.name,
          "selectedList",
          "refName:",
          refName,
          ", Existed?",
          !!this.$refs[refName][0]
        );
      } else {
        this.$warn(
          this.$options.name,
          "selectedList",
          "refName:",
          refName,
          ", Existed?",
          !!this.$refs[refName][0]
        );
      }
    },

    /**
     * All deselected. Change All item Selected color to Deselected color.
     * @public
     * @param {null}
     */
    allDeselected: function() {
      if (this.lists) {
        for (var list of this.lists) {
          var mainRef = list.title ? "main_" + list.title : "main_" + list.name;
          if (this.$refs[mainRef][0]) {
            this.$refs[mainRef][0].$el.style.backgroundColor = this.DESELECTED;
          }
          if (list.submenu) {
            for (var i = 0; i < list.submenu.length; ++i) {
              var subRef = list.submenu[i].title
                ? "sub_" + list.submenu[i].title
                : "sub_" + list.submenu[i].name;
              if (this.$refs[subRef][0]) {
                this.$refs[
                  subRef
                ][0].$el.style.backgroundColor = this.DESELECTED;
              }
            }
          }
          if (list.expands) {
            for (var k = 0; k < list.expands.length; ++k) {
              var expandsRef = list.expands[k].title
                ? "expand_" + list.expands[k].title
                : "expand_" + list.expands[k].name;
              if (this.$refs[expandsRef][0]) {
                this.$refs[
                  expandsRef
                ][0].$el.style.backgroundColor = this.DESELECTED;
              }
            }
          }
        }
      }
    },

    /**
     * Click Event of Header.
     * @public
     * @param {object} - header`s data.
     */
    onClickHeader: function(header) {
      /**
       * Header click Event.
       * @event headerClick
       * @type {emit}
       * @property {object} - main item.
       */
      this.$emit("headerClick", header);
    },

    /**
     * Click Event of Main item.
     * @public
     * @param {object} - main item`s data.
     */
    onClickMainList: function(mainItem) {
      var refName = mainItem.title
        ? "main_" + mainItem.title
        : "main_" + mainItem.name;
      this.selectedList(refName);
      /**
       * main item click Event.
       * @event mainClick
       * @type {emit}
       * @property {object} - main item.
       */
      this.$emit("mainClick", mainItem);
    },

    /**
     * Click Event of MainGroup item.
     * @public
     * @param {object} - main group item`s data.
     */
    onClickMainGroupList: function(mainGroupItem) {
      mainGroupItem.active = !mainGroupItem.active;
      this.$store.commit("project/toggleListActive", { item: mainGroupItem });
      /**
       * main group item click Event.
       * @event mainGroupClick
       * @type {emit}
       * @property {object} - main group item.
       */
      this.$emit("mainGroupClick", mainGroupItem);
    },

    /**
     * Click Event of sub item.
     * @public
     * @param {object} - sub item`s data.
     * @param {object} - sub item`s parent(main item)`s data.
     */
    onClickSubList: function(subItem, list) {
      var refName = subItem.title
        ? "sub_" + subItem.title
        : "sub_" + subItem.name;
      this.selectedList(refName);
      var event = { list: list, subItem: subItem };
      /**
       * sub item click Event.
       * @event subClick
       * @type {emit}
       * @property {object} - main item and sub item.
       */
      this.$emit("subClick", event);
    },

    /**
     * Click Event of expand item.
     * @public
     * @param {object} - expand item`s data.
     * @param {object} - expand item`s parent(main item)`s data.
     */
    onClickExpandList: function(expandItem, list) {
      var event = { list: list, expandItem: expandItem };
      /**
       * expand item click Event.
       * @event expandClick
       * @type {emit}
       * @property {object} -  main item and expand item.
       */
      this.$emit("expandClick", event);
    },
  },

  created() {},
  mounted() {},
};
</script>

<style scoped>
.answer-list {
  width: 100%;
  height: 100%;
}
.list-style {
  padding-top: 0;
}
.header-avatar {
  border: 1px solid;
}
.header-avatar-text {
  min-width: 32.5px;
}
.header-text {
  font-size: 18px;
}
.fit-font {
  word-break: break-all;
  white-space: nowrap;
  font-size: 90%;
  font-weight: bold;
}
</style>
