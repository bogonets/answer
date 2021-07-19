import Vue from 'vue'
import VueI18n from 'vue-i18n';
import en from '@/translations/lang/en'
import ko from '@/translations/lang/ko'

Vue.use(VueI18n)

const options = {
  messages: {
    en: en,
    ko: ko,
  },
};

export default new VueI18n(options);
