<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component
export default class App extends Vue {
  beforeCreate() {
    const dark = this.$localStore.getters['theme/getTheme'] as boolean;
    const lang = this.$localStore.getters['language/getLanguage'] as string;
    const api = this.$localStore.getters['etc/getApiUrl'] as string;

    this.$vuetify.theme.dark = dark;
    this.$vuetify.lang.current = lang;
    this.$i18n.locale = lang;
    this.$api.setUrl(api);
    this.$api2.origin = api;
  }
}
</script>
