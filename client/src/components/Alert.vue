<template>
  <div class="alert alert-danger d-flex align-items-center" role="alert">
    <div>
      {{ message }}
    </div>
  </div>
</template>

<script>
export default {
  props: ['message'],
};
</script>
