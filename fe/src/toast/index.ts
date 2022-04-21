import Vue from 'vue';
import Toast from 'vue-toastification';
import '@/toast/style.scss';

const options = {
  maxToasts: 20,
  newestOnTop: true,
  position: 'bottom-right',
};

Vue.use(Toast, options);
