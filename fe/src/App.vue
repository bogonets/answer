<template>
  <v-app :dark="dark">
    <transition name="slide" mode="out-in">
      <router-view />
    </transition>
  </v-app>
</template>

<script lang="ts">
import { Vue, Component, Watch } from "vue-property-decorator"

@Component
export default class App extends Vue {
  created() {
    // this.$api.setUrl(this.$local.getters['etc/getApiUrl']);
  }

  mounted() {
    this.$vuetify.lang.current = "ko";
    this.$i18n.locale = this.$store.getters["language/getLanguage"];
    this.$api.setUrl(this.$localStore.getters["etc/getApiUrl"]);
  }

  beforeDestroy() {
    // EMPTY.
  }

  get dark(): boolean {
    return this.$vuetify.theme.dark;
  }

  @Watch("dark")
  onChangedDark() {
    this.$vuetify.theme.dark = this.dark;
  }
}
</script>

<style lang="scss">
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
