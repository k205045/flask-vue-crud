<template>
  <div>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 text-center mb-5">
          <h2 class="heading-section"></h2>
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-md-7 col-lg-5">
          <div class="login-wrap p-4 p-md-5">
            <div class="icon d-flex align-items-center justify-content-center">
              <span class="fa fa-user-o"></span>
            </div>
            <h3 class="text-center mb-4">Sign In</h3>
            <form @submit.prevent="login" class="login-form">
              <div class="form-group">
                <input type="text" class="form-control rounded-left" placeholder="userName"
                v-model="userName" required>
              </div>
              <div class="form-group d-flex">
                <input type="password" class="form-control rounded-left" placeholder="password"
                v-model="password" required>
              </div>
              <div class="form-group">
                <button type="submit"
                class="form-control btn btn-primary rounded submit px-3">Login</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userName: '',
      password: '',
    };
  },
  methods: {
    login() {
      if (this.username === '' || this.password === '') {
        // eslint-disable-next-line
        alert('請輸入使用者名稱或者密碼');
      } else {
        const params = new URLSearchParams();
        params.append('username', this.username);
        params.append('password', this.password);
        this.axios.post('http://127.0.0.1:5000/login', params).then((res) => {
          // eslint-disable-next-line
          console.log(res.data);
          // eslint-disable-next-line
          console.log(typeof res.data);
          if (res.data === 0) {
            // eslint-disable-next-line
            alert('login failed');
          } else {
            localStorage.setItem('token', 'ImLogin');
            this.$router.replace({ name: 'Home' });
          }
        });
      }
    },
  },
};
</script>
