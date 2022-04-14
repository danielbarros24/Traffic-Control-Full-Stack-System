<template>
  <v-app id="inspire">
    <v-content>
      <v-container class="fill-height">
        <v-row align="center" justify="center">
          <v-col cols="7" md="4">
            <v-card class="elevation-12">
              <v-window v-model="step">
                  <v-card-text class="pt-9 pl-10 pr-16 pb-10" flat>
                    <v-img
                      class="mb-12 mx-auto text-center"
                      src="../assets/logo.png"
                      max-height="160"
                      max-width="160"
                    ></v-img>

                    <v-form>
                      <v-text-field
                        v-model="username"
                        label="Username"
                        name="username"
                        prepend-icon="mdi-account"
                        type="text"
                        color="deep-purple darken-3"
                      />
                      <v-text-field
                        v-model="password"
                        id="password"
                        label="Password"
                        name="password"
                        prepend-icon="key"
                        type="password"
                        color="deep-purple darken-3"
                        :rules="[v => !!v || 'You must type password!']"
                      />
                      <v-btn v-on:click="signIn" rounded color="deep-purple darken-3" class="mt-4" block dark 
                      >SIGN IN</v-btn
                    >
                    </v-form>

                  </v-card-text>
              </v-window>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    step: 1,
    age: 11,
    username:'',
    password:''
  }),
  props: {
    source: String,
  },

  methods:{
    signIn() {
      console.log("Logged in")
      this.$router.push("dashboard");
    }
  },

  async mounted() {
    const response = await fetch("http://127.0.0.1:5000/")

    const data = await response.json()
    console.log(data)

    this.age = data.idade
  }
};

</script>

<style>
.v-content {
  background: rgb(63, 154, 251);
  background: radial-gradient(
    circle,
    rgba(63, 154, 251, 1) 0%,
    rgba(140, 91, 251, 1) 45%,
    rgba(126, 70, 252, 1) 100%
  );
}

.v-card {
  background: transparent;
}
</style>