import Vue from 'vue';
import Router from 'vue-router';
// import Ping from '@/components/Ping';
// import Addrs from '@/components/Addrs';
import Login from '@/components/Login';
import Home from '@/components/Home';
import Header from '@/components/Header';
import UserInfo from '@/components/UserInfo';

Vue.use(Router);

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'Addrs',
//       component: Addrs,
//     },
//     {
//       path: '/ping',
//       name: 'Ping',
//       component: Ping,
//     },
//   ],
//   mode: 'history',
// });
export default new Router({
  routes: [
    {
      path: '*',
      redirect: '/',
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
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
