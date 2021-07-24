<i18n lang="yaml">
en:
  lang_name: "English"
  title: "Appearance"
  subtitle: "Customize the look and feel of your Answer."
  theme:
    header: "Theme"
    dark:
      title: "Dark Mode"
      subtitle: "Apply a theme that displays white text on a dark screen."
  i18n:
    header: "Internationalization"
    lang:
      title: "Language"
      subtitle: "It will be translated into your preferred language."

ko:
  lang_name: "한글"
  title: "외관"
  subtitle: "Answer의 모양과 느낌을 설정할 수 있습니다."
  theme:
    header: "테마"
    dark:
      title: "어두운 화면"
      subtitle: "어두운 화면에 흰 글자를 나타내는 테마를 적용합니다."
  i18n:
    header: "국제화"
    lang:
      title: "언어"
      subtitle: "원하는 언어로 번역됩니다."
</i18n>

<template>
  <v-container>
    <v-list three-line>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            {{ $t('title') }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ $t('subtitle') }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list flat subheader three-line>
      <v-subheader>{{ $t('theme.header') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('theme.dark.title') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('theme.dark.subtitle') }}</v-list-item-subtitle>
        </v-list-item-content>

        <v-switch inset v-model="extra.dark" @change="changeDark"></v-switch>
      </v-list-item>

      <v-subheader>{{ $t('i18n.header') }}</v-subheader>

      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>{{ $t('i18n.lang.title') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('i18n.lang.subtitle') }}</v-list-item-subtitle>
        </v-list-item-content>

<!--        <v-list dense>-->
<!--          <v-list-item-group-->
<!--              mandatory-->
<!--              color="primary"-->
<!--              :value="currentLangIndex"-->
<!--              @change="changeLangIndex"-->
<!--          >-->
<!--            <v-list-item v-for="lang in languages" :key="lang">-->
<!--              <v-list-item-content>-->
<!--                <v-list-item-title v-text="$t('name', lang)"></v-list-item-title>-->
<!--              </v-list-item-content>-->
<!--            </v-list-item>-->
<!--          </v-list-item-group>-->
<!--        </v-list>-->
      </v-list-item>

    </v-list>
  </v-container>
</template>

<script lang="ts">
import VueI18n from '@/translations/VueI18n';
import { Component } from 'vue-property-decorator';
import MenuTranslate from '@/components/MenuTranslate.vue';
import { Extra } from '@/apis/api-v2';

@Component({
  components: {
    MenuTranslate
  }
})
export default class AppearancePage extends VueI18n {

  extra!: Extra;

  beforeCreate() {
    const extra = this.$localStore.user.extra;
    if (extra) {
      this.extra = extra;
    } else {
      this.extra = {} as Extra;
    }

    if (this.extra.dark === undefined) {
      this.extra.dark = this.$localStore.dark;
    }
    if (this.extra.lang === undefined) {
      this.extra.lang = this.$localStore.lang;
    }
  }

  saveUserExtra() {
    this.$api2.putSelfExtra(this.extra)
        .then(() => {
          console.debug('Storing user extra information was successful.');
        })
        .catch(error => {
          console.error(error);
        });
  }

  changeDark() {
    const dark = this.extra.dark;
    if (dark !== undefined) {
      this.$localStore.dark = dark;
      this.$vuetify.theme.dark = dark;
    }

    this.saveUserExtra();
  }

  changeLangIndex(index: string) {
    this.saveUserExtra();
  }
}
</script>
