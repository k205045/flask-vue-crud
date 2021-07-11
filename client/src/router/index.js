import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/login/login';
import Home from '@/views/home/Addr';
import Header from '@/components/Header';
import vSelect from 'vue-select';

Vue.component('v-select', vSelect);
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/home',
      name: 'Home',
      components: {
        default: Home,
        nav: Header,
      },
    },
  ],
  mode: 'history',
});
