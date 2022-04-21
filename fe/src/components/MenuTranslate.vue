<i18n lang="yaml">
en:
  header: "Translations"

ko:
  header: "언어선택"
</i18n>

<template>
  <v-menu open-on-hover transition="slide-y-transition" :offset-y="true">
    <template v-slot:activator="{on, attrs}">
      <v-btn icon small v-bind="attrs" v-on="on">
        <v-icon small aria-hidden="false">
          mdi-translate
        </v-icon>
      </v-btn>
    </template>

    <list-languages
      dense
      :header="$t('header')"
      :init-lang="initLang"
      :init-vuetify="initVuetify"
      :init-local-store="initLocalStore"
      :init-user-extra="initUserExtra"
      @change-lang="changeLang"
    ></list-languages>
  </v-menu>
</template>

<script lang="ts">
import VueI18n from '@/translations/VueI18n';
import {Component, Prop, Emit} from 'vue-property-decorator';
import ListLanguages from '@/components/ListLanguages.vue';

@Component({
  components: {
    ListLanguages,
  },
})
export default class MenuTranslate extends VueI18n {
  @Prop({type: String, default: ''})
  readonly initLang!: string;

  @Prop({type: Boolean, default: false})
  readonly initVuetify!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initLocalStore!: boolean;

  @Prop({type: Boolean, default: false})
  readonly initUserExtra!: boolean;

  @Emit()
  changeLang(lang: string) {
    return lang;
  }
}
</script>
