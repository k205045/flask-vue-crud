import Vue from 'vue';
import Router from 'vue-router';
import Addrs from '@/components/Addrs';
import Login from '@/components/Login';
import Header from '@/components/Header';
import UserInfo from '@/components/UserInfo';
import vSelect from 'vue-select';

Vue.component('v-select', vSelect);
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '*',
      redirect: '/',
    },
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/Addr',
      name: 'Addr',
      components: {
        default: Addrs,
        nav: Header,
      },
    },
    {
      path: '/userInfo',
      components: {
        default: UserInfo,
        nav: Header,
      },
    },
  ],
  mode: 'history',
});
