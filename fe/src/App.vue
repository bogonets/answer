<template>
  <v-app :dark="dark">
    <router-view />
  </v-app>
</template>

<script lang="ts">
import { Vue, Component, Watch } from 'vue-property-decorator'

@Component
export default class App extends Vue {
  mounted() {
    const storedLanguage = this.$store.getters['language/getLanguage']
    const language = storedLanguage ? storedLanguage : 'ko';
    this.$vuetify.lang.current = language;
    this.$i18n.locale = language;

    const storedApiOrigin = this.$localStore.getters['etc/getApiUrl'];
    const apiOrigin = storedApiOrigin ? storedApiOrigin : document.location.origin;
    this.$api.setUrl(apiOrigin);
    this.$api2.origin = apiOrigin;
  }

  get dark(): boolean {
    return this.$vuetify.theme.dark;
  }

  @Watch('dark')
  onChangedDark() {
    this.$vuetify.theme.dark = this.dark;
  }
}
</script>

<style lang="scss">

html {
  overflow: hidden !important;
  -ms-overflow-style: none;
}

html::-webkit-scrollbar {
  width: 0;
  height: 0;
}

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
