<template>
  <div>
    <v-menu
      open-on-click
      :close-on-content-click="true"
      left
      bottom
      offset-y
      transition="v-menu-transition"
      :z-index="500"
      :dark="this.$vuetify.theme.dark"
    >
      <template v-slot:activator="{ on }">
        <v-btn icon v-on="on">
          <v-icon class="btn-icon-style">account_circle</v-icon>
        </v-btn>
      </template>
      <v-list dense>
        <v-list-item class="info-style">
          <v-list-item-icon>
            <v-icon>account_circle</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-html="myid"></v-list-item-title>
            <!-- <v-list-tile-sub-title>{{ version }}</v-list-tile-sub-title> -->
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item @click="gotoSettingPage">
          <v-list-item-icon>
            <v-icon>settings</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("setting") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item @click="onClickLogout()">
          <v-list-item-icon>
            <v-icon>exit_to_app</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t("logout") }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog
      v-model="openSetting"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <setting-page @close="openSetting = !openSetting"></setting-page>
    </v-dialog>
  </div>
</template>

<script>
import SettingPage from "@/components/Setting/AnswerSetting.vue";
/**
 * User menu.
 * @author hadoo, 2019-03-02
 */
export default {
  name: "adbUserBox",
  props: {},
  components: {
    SettingPage,
  },
  data() {
    return {
      openSetting: false,
    };
  },
  methods: {
    /**
     * Go to Setting page Event.
     * @public
     */
    gotoSettingPage: function() {
      this.openSetting = true;
    },

    /**
     * This is Logout Event.
     * @public
     */
    onClickLogout: function() {
      this.$localStore.clearSession();
      this.$store.commit("user/logout");
      this.$router.push("/");
      this.$debug(this.$options.name, "onLogout", "LOGOUT!");
    },
  },
  computed: {
    myid() {
      // Get from User session storage.
      // This data is passed to UserBox.vue of Titlebar.vue.
      return this.$store.getters["user/getUserID"];
    },
    myemail() {
      // Get from User session storage.
      // This data is passed to UserBox.vue of Titlebar.vue.
      return this.$store.getters["user/getUserEmail"];
    },
  },
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

/* Transition */
.fade-enter-active {
  transition: opacity 0.5s;
}
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
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
