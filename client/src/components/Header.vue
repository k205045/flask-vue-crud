<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <span class="navbar-brand mb-0 h1">Keyence Monitor</span>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
      data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
      aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <!-- <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/Addr">Home</a>
        </li> -->
        <!-- <li class="nav-item">
          <a class="nav-link active" href="/UserInfo">User Info</a>
        </li> -->
      </ul>
      <a class="nav-link active d-flex ml-auto" aria-current="page" href=""
      @click.prevent="logout">Logout</a>
    </div>
  </div>
</nav>

</template>
<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
  },
};
</script>
