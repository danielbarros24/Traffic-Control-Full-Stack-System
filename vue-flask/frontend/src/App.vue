<template>
  <v-app>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'App',

  data: () => ({
    //
  }),
  computed: {
    ...mapGetters(["isLoggedIn"]),
  }
};
</script>

<style>

.v-main {
  background-image: linear-gradient(
  180deg,
  hsl(200deg 100% 37%) 0%,
  hsl(209deg 50% 60%) 70%,
  hsl(211deg 49% 74%) 86%,
  hsl(213deg 49% 87%) 93%,
  hsl(0deg 0% 100%) 100%
);
}

</style>