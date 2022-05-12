<template>
  <v-app>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style>

.v-main {
  background: rgb(63, 154, 251);
  background: radial-gradient(
    circle,
    rgba(63, 154, 251, 1) 0%,
    rgba(140, 91, 251, 1) 45%,
    rgba(126, 70, 252, 1) 100%
  );
}

</style>