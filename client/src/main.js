import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App';
import router from './router';
/* eslint-disable */
Vue.config.productionTip = false;

Vue.use(BootstrapVue);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});

router.beforeEach((to, from, next) => {
  const isLogin = localStorage.getItem('token') === 'ImLogin';
  if (isLogin) {
    next();
  } else {
    if (to.path !== '/login') {
      next('/login');
    } else {
      next();
    }
  }
});
