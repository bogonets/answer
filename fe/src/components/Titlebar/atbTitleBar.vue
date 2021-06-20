<template>
  <v-app-bar
    fixed
    app
    dense
    :extended="loadingbar"
    extension-height="0.5"
    :clipped-left="true"
    :clipped-right="true"
  >
    <v-app-bar-nav-icon @click.stop="openMenu"></v-app-bar-nav-icon>
    <app-title :title="'answer'" :upperCase="true" :fontSize="28" :textShadow="'2px 2px grey'"></app-title>
    <!-- <v-toolbar-title class="title-style">{{ title }}</v-toolbar-title> -->
    <!-- 현재 사용하지 않는 버튼 3가지 추후 사용될 예정-->
    <v-btn
      class="page-btn"
      small
      text
      color="info"
      @click="gotoProjects"
      >projects</v-btn
    >
    <v-btn
      v-show="!disable"
      :disabled="disable"
      class="page-btn"
      small
      text
      color="#0000ff"
      @click="gotoGroups"
      >groups</v-btn
    >
    <v-btn
      v-show="!disable"
      :disabled="disable"
      class="page-btn"
      small
      text
      color="#ff00f0"
      @click="gotoAdmin"
      >admin</v-btn
    >
    <v-spacer />
    <!-- <v-btn small fab icon @click="$emit('openConsole')"><v-icon size="20">fas fa-terminal</v-icon></v-btn> -->
    <adb-user-box
      ref="userbox"
    />
    <template v-if="loadingbar" v-slot:extension>
      <v-progress-linear
        :indeterminate="loadingbar"
        height="1"
        color="#ffffff"
      />
    </template>
  </v-app-bar>
</template>

<script>
import adbUserBox from "@/components/Dropbox/adbUserBox";
/**
 * Asnwer Main Titlebar component.
 * @author hadoo, 2019-06-16
 */

export default {
  components: {
    adbUserBox
  },
  props: {
    /**
     * Title Name.
     */
    title: { type: String, default: "Answer" }
  },
  data() {
    return {
      disable: true,
      loadingbar: false
    };
  },
  methods: {
    /**
     * Go to projectsMain Page.
     * @public
     */
    gotoProjects: function() {
      this.$router.push(this.$page.projects);
    },
    /**
     * Go to GroupsMain Page.
     * @public
     */
    gotoGroups: function() {
      this.$router.push(this.$page.groups);
    },
    /**
     * Go to AdminMain Page.
     * @public
     */
    gotoAdmin: function() {
      this.$router.push(this.$page.admin);
    },
    /**
     * Side bar menu open and close. Save in Store.
     * @public
     */
    openMenu: function() {
      if (this.$store.getters["drawer/getNaviWidth"] == 200) {
        this.$store.commit("drawer/setNaviWidth", { width: 55 });
      } else {
        this.$store.commit("drawer/setNaviWidth", { width: 200 });
      }
      /**
       * Other Method. Show And Hide.
       */
      // if (this.$store.getters['drawer/getNaviShow']) {
      // 	this.$store.commit('drawer/setNaviShow', {bool: false});
      // } else {
      // 	this.$store.commit('drawer/setNaviShow', {bool: true});
      // }
    }
  },
  computed: {
    loading_liner() {
      return this.$store.getters["etc/getLoadingLiner"];
    }
  },
  watch: {
    loading_liner() {
      setTimeout(() => {
        this.loadingbar = this.loading_liner;
      }, 500);
    }
  }
};
</script>

<style>
.page-btn {
  margin-top: 18px;
  margin-right: 0px;
  margin-left: 0px;
  font-size: 8px;
}
.title-style {
  font-size: 30px;
  margin-left: 15px;
  /* margin-left: -10px; */
  /* margin-right: 20px; */
}
.no-drag {
  -ms-user-select: none;
  -moz-user-select: -moz-none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  user-select: none;
}
v-toolbar > v-progress-liner {
  margin-left: 50px;
}
</style>
