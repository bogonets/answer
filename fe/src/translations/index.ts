import Vue from 'vue'
import VueI18n from 'vue-i18n';
import en from '@/translations/lang/en'
import ko from '@/translations/lang/ko'

Vue.use(VueI18n);

const DEFAULT_LOCALE = process.env.ANSWER_I18N_LOCALE || 'en';
const DEFAULT_FALLBACK_LOCALE = process.env.ANSWER_I18N_FALLBACK_LOCALE || 'en';

const i18n = new VueI18n({
  locale: DEFAULT_LOCALE,
  fallbackLocale: DEFAULT_FALLBACK_LOCALE,
  messages: {
    en: en,
    ko: ko,
  },
});

export default i18n;
