<template>
  <v-menu :dark="$store.getters['theme/getTheme']" left offset-y open-on-hover>
    <template v-slot:activator="{ on }">
      <v-btn class="border-style" left v-on="on">
        <v-icon class="icon-margin">invert_colors</v-icon>
        {{ select_theme }}
      </v-btn>
    </template>
    <v-list class="border-style">
      <v-list-item
        v-for="(theme, index) in themes"
        :key="index"
        @click="onTheme(index)"
      >
        <v-list-item-title>{{ theme }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
/**
 * Answer Combobox For Theme Change(Light, Dark from Vuetify)
 * @author hadoo 2019-06-26
 */

export default {
  name: "acbThemeChanger",
  data() {
    return {
      select_theme: "",
      themes: ["dark", "light"],
    };
  },
  methods: {
    /**
     * Change Theme Method.
     * @param {string} - theme value 'dark' or 'light'
     * @public
     */
    onTheme: function(index) {
      if (index == 1) {
        this.select_theme = this.themes[1];
        this.$vuetify.theme.dark = false;
      } else {
        this.select_theme = this.themes[0];
        this.$vuetify.theme.dark = true;
      }
    },
  },
  // Initialize ThemeChanger.
  created() {
    if (this.$vuetify.theme.dark) {
      this.select_theme = this.themes[0];
    } else {
      this.select_theme = this.themes[1];
    }
  },
};
</script>

<style scoped>
.icon-margin {
  padding: 0px 0px 0px 0px;
  margin-right: 10px;
}
</style>
