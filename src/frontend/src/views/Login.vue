<template>
  <v-app id="inspire">
    <v-main>
      <v-container class="fill-height">
        <v-row align="center" justify="center">
          <v-col cols="7" md="4">
            <v-card class="elevation-12">
              <v-window>
                  <v-card-text class="pt-9 pl-10 pr-16 pb-10" flat>
                    <v-img
                      class="mb-12 mx-auto text-center"
                      src="../assets/logo.png"
                      max-height="160"
                      max-width="160"
                    ></v-img>

                    <v-form ref="form"
                      v-model="valid"
                      lazy-validation>
                      <v-text-field
                        v-model="username"
                        label="Username"
                        name="username"
                        prepend-icon="mdi-account"
                        type="text"
                        color="primary"
                        required
                        :rules="[v => !!v || 'You must type username!']"
                      />
                      <v-text-field
                        v-model="password"
                        id="password"
                        label="Password"
                        name="password"
                        prepend-icon="key"
                        type="password"
                        color="primary"
                        :rules="[v => !!v || 'You must type password!']"
                      />
                      <v-btn @click="postData" rounded color="primary" class="mt-4" block dark 
                      >SIGN IN</v-btn
                    >
                    <p class="red--text mt-3 mr-6" v-show="invalidCredentials" >
                      Invalid Credentials!
                    </p>
                    </v-form>
                  </v-card-text>
              </v-window>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  data: () => ({
    username:'',
    password:'',
    valid: true,
    invalidCredentials: false,
  }),
  props: {
    source: String,
  },

  methods:{
    async postData() {
      this.$refs.form.validate()
      const authData = {
        username: this.username,
        password: this.password,
      }

      this.$store.dispatch('login', authData).then(() => {
			  this.$router.push('/dashboard');  
			});
      //console.log(data)

    },
    clearPostOutput() {
      this.postResult = null;
    }
  },
};

</script>

<style>
</style>