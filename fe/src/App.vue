<template>
  <v-app :dark="dark">
    <transition name="slide" mode="out-in">
      <router-view />
    </transition>
  </v-app>
</template>

<script>
/**
 * 앱 자체의 모듈입니다. main에서 생성되는 루트 vue에 사용됩니다.
 * @author zilhak, 2019-01-09
 *
 * @param {router-view} - 메인 라우터입니다.
 */
export default {
  name: "App",
  components: {},
  data() {
    return {};
  },
  methods: {},
  computed: {
    dark() {
      return this.$vuetify.theme.dark;
    },
  },
  watch: {
    dark() {
      this.$vuetify.theme.dark = this.dark;
    },
  },
  created() {
    // this.$api.setUrl(this.$local.getters['etc/getApiUrl']);
  },
  mounted() {
    this.$vuetify.lang.current = "ko";
    this.$i18n.locale = this.$store.getters["language/getLanguage"];
    this.$api.setUrl(this.$localStore.getters["etc/getApiUrl"]);
  },
  beforeDestroy() {},
};
</script>

<style>
.slide-leave-active {
  transition: opacity 0.1s, transform 0.1s;
  transform: translateX(-10%);
  opacity: 0;
}

.slide-enter-active {
  transition: opacity 0.1s, transform 0.1s;
  transform: translateX(0%);
}

.slide-enter {
  opacity: 0;
  transform: translateX(10%);
}
/**
 * Overlay of Vuetify Dialog Opacity style.
 */
.v-dialog__content--active {
  background-color: rgba(0, 0, 0, 0.7) !important;
}
</style>
