<template>
  <v-card
    :style="
      this.$vuetify.theme.dark
        ? 'background-color: #191919'
        : 'background-color: #F5F5F5'
    "
  >
    <v-app-bar dense flat class="toolbar elevation-15">
      <v-app-bar-nav-icon @click="showMenu = !showMenu"></v-app-bar-nav-icon>
      <span class="headline">{{ $t("setting") }}</span>
      <v-spacer></v-spacer>
      <slot name="options">
        <v-btn text icon @click="onClose" :title="$t('close')">
          <v-icon>close</v-icon>
        </v-btn>
      </slot>
    </v-app-bar>
    <div class="content">
      <v-row no-gutters class="content--row">
        <v-col class="flex-grow-0 flex-shrink-1">
          <transition name="slide-fade">
            <v-card v-if="showMenu" class="navigation elevation-20">
              <a-list
                :lists="menus"
                :i18nMain="true"
                @mainClick="mvSettingPage($event)"
              ></a-list>
            </v-card>
          </transition>
        </v-col>
        <v-col class="flex-grow-1 flex-shrink-0">
          <v-card class="page elevation-0">
            <v-container fluid class="pa-10" style="height: 100%;">
              <div v-if="currentPage === 'general_setting'">
                <v-row>
                  <v-flex xs12 class="ma-bt-10">
                    <v-card>
                      <v-card-title id="title">
                        <strong>{{ $t("language") }}</strong>
                        <v-spacer></v-spacer>
                        <acb-language-changer></acb-language-changer>
                      </v-card-title>
                    </v-card>
                  </v-flex>
                  <v-flex xs12 class="ma-bt-10">
                    <v-card>
                      <v-card-title id="title">
                        <strong>{{ $t("theme") }}</strong>
                        <v-spacer></v-spacer>
                        <acb-theme-changer></acb-theme-changer>
                      </v-card-title>
                    </v-card>
                  </v-flex>
                  <v-flex xs12 class="ma-bt-10">
                    <v-card>
                      <v-card-title id="title">
                        <strong>{{ $t("lambda_template") }}</strong>
                        <v-spacer></v-spacer>
                        <acb-lambda-templates-renewal></acb-lambda-templates-renewal>
                      </v-card-title>
                    </v-card>
                  </v-flex>
                </v-row>
              </div>
              <div v-else-if="currentPage === 'members_manage'">
                <v-row>
                  <v-flex xs12 class="ma-bt-10">
                    <v-card>
                      <members></members>
                    </v-card>
                  </v-flex>
                </v-row>
              </div>
              <version
                v-else-if="currentPage === 'information_view'"
                :useContainer="false"
              ></version>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script>
import acbLanguageChanger from "@/components/Combobox/acbLanguageChanger";
import acbThemeChanger from "@/components/Combobox/acbThemeChanger";
import acbLambdaTemplatesRenewal from "@/components/Combobox/acbLambdaTemplatesRenewal";
import Version from "@/pages/Info/Version.vue";
import Members from "@/components/Table/aUserTable.vue";

export default {
  name: "AnswerSetting",
  props: {},
  components: {
    acbLanguageChanger,
    acbThemeChanger,
    acbLambdaTemplatesRenewal,
    Version,
    Members,
  },
  data() {
    return {
      showMenu: true,
      menus: [
        {
          title: "general_setting",
          icon: "settings",
        },
        {
          title: "members_manage",
          icon: "group",
        },
        {
          title: "information_view",
          icon: "info",
        },
      ],
      currentPage: "general_setting",
    };
  },
  computed: {},
  methods: {
    /**
     * If used at dialog, make close event.
     * @public
     */
    onClose: function() {
      this.$emit("close");
    },

    /**
     * Move 'general, members, information' page in Setting Dialog.
     * @public
     */
    mvSettingPage: function(pageName) {
      this.currentPage = pageName.title;
    },
  },
  created() {},
  mounted() {},
};
</script>

<style scoped>
.toolbar {
  margin: 0;
}
.content {
  position: absolute;
  top: 48px;
  width: 100%;
  height: calc(100% - 48px);
}
.content--row {
  height: 100%;
  max-height: 100%;
  overflow-y: auto;
}
.navigation {
  height: 100%;
  min-width: 200px;
}
.page {
  height: 100%;
  background-color: transparent;
}
.ma-bt-10 {
  margin-bottom: 10px;
}
.slide-fade-enter-active {
  transition: all 0.15s linear;
}
.slide-fade-leave-active {
  /* transition: all 0.15s cubic-bezier(1, 0.5, 0.5, 1); */
  transition: all 0.15s linear;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(-10px);
  /* opacity: 0; */
}
</style>
