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
        <li class="nav-item">
          <a class="nav-link active" aria-current="page"
          type="button" @click="Save()">Save Setting</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active"  type="button" @click="Load()">
            Load Setting</a>
        </li>
      </ul>
      <a class="nav-link active d-flex ml-auto" aria-current="page" href=""
      @click.prevent="logout">Logout</a>
    </div>
  </div>
</nav>

</template>
<script>
import axios from 'axios';

export default {
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    Save() {
      const path = 'http://localhost:5000/save';
      axios.post(path)
        .then(() => {
          // eslint-disable-next-line
          alert('Save Success');
        })
        .catch((error) => {
          // eslint-disable-next-line
          alert('Save failed');
          // eslint-disable-next-line
          console.error(error);
        });
    },
    Load() {
      const path = 'http://localhost:5000/load';
      axios.post(path)
        .then(() => {
          // eslint-disable-next-line
          alert('Load Success');
        })
        .catch((error) => {
          // eslint-disable-next-line
          alert('Load failed');
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
