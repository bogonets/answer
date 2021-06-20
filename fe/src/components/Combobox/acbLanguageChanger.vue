<template>
  <v-menu :dark="this.$vuetify.theme.dark" left offset-y open-on-hover>
    <template v-slot:activator="{ on }">
      <v-btn class="border-style" left v-on="on">
        <v-icon class="icon-margin">language</v-icon>
        {{ $t(select_lang) }}
      </v-btn>
    </template>
    <v-list class="border-style">
      <v-list-item
        v-for="(lang, index) in langs"
        :key="index"
        @click="onLanguage(lang.state)"
      >
        <!-- <div :class="lang.state + '-icon'" style="width: 20px; height: 20px; border:1px solid white;"></div> -->
        <!-- <img v-if="lang.state === 'ko'" src="@/assets/ko.svg" alt="korea" width="20px" height="20px"/>
				<img v-else-if="lang.state === 'en'" src="@/assets/en.svg" alt="korea" width="20px" height="20px"/> -->
        <v-list-item-title>{{ lang.val }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
/**
 * Answer Combobox For Language Change.
 * @author hadoo 2019-06-26
 */

export default {
  name: "acbLanguageChanger",
  data() {
    return {
      select_lang: "",
      langs: [],
    };
  },
  methods: {
    /**
     * Language change method.
     * @public
     * @param {string} - language value ex) ex, ko
     */
    onLanguage: function(value) {
      this.$i18n.locale = value;
      this.select_lang = value;
      this.$store.commit("language/setLanguage", { language: value });
      this.$vuetify.lang.current = value;
    },
  },
  // Initialize the value before LanguageChanger is generated.
  created: function() {
    this.select_lang =
      this.$store.getters["language/getLanguage"] || this.$i18n.locale;
    this.langs = [
      { state: "en", val: this.$t("en") },
      { state: "ko", val: this.$t("ko") },
    ];
  },
};
</script>

<style>
.select-style {
  color: #0000ff !important;
  -webkit-text-fill-color: chartreuse;
}
.select-item-style {
  -webkit-text-fill-color: #ff0000 !important;
}
.icon-margin {
  padding: 0px 0px 0px 0px;
  margin-right: 10px;
}
</style>
