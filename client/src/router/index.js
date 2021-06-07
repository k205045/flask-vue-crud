import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Addrs from '@/components/Addrs';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Addrs',
      component: Addrs,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
  mode: 'history',
});
