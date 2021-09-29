import Vue from 'vue';
import VueRouter from 'vue-router';
import routes from '@/router/routes';

Vue.use(VueRouter);

export const router = new VueRouter({
  routes: routes,
  mode: 'history',
});
export default router;
