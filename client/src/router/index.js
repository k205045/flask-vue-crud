import Vue from 'vue';
import Router from 'vue-router';
import Login from '@/views/login/login';
import Home from '@/views/home/Addr';
import Header from '@/components/Header';
import vSelect from 'vue-select';

Vue.component('v-select', vSelect);
Vue.use(Router);

const router = new Router({
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
      name: 'Home',
      components: {
        default: Home,
        nav: Header,
      },
    },
  ],
  mode: 'history',
});

router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem('token') === 'ImLogin';
  if (isLogin) {
    next();
  } else if (to.path !== '/') {
    // eslint-disable-next-line
    alert('請先登入');
    next('/');
  } else {
    next();
  }
});

export default router;
