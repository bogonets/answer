import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from '@/router/routes';

Vue.use(VueRouter);

export const router = new VueRouter({
  routes: routes,
  mode: process.env.IS_ELECTRON ? 'hash' : 'history',
});
export default router;
