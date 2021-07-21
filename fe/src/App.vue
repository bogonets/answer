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
    const dark = this.$localStore.dark;
    const lang = this.$localStore.lang;
    const api = this.$localStore.origin;

    this.$vuetify.theme.dark = dark;
    this.$vuetify.lang.current = lang;
    this.$i18n.locale = lang;
    this.$api.setUrl(api);
    this.$api2.origin = api;
  }
}
</script>
