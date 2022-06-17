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
                      <v-btn @click="postData()" rounded color="primary" class="mt-4" block dark 
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
      const postData = {
        username: this.username,
        password: this.password,
      }
      try {
        const urlDesktop = "127.0.0.1:5000"
        const urlRasp = "192.168.1.216:8080"
        
        const res = await fetch(`http://${urlDesktop}/login`, {
          method: "POST",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8'
          },
          body: JSON.stringify(postData),
        })

        const data = await res.json();
        console.log(data)

        if (data.access != "ok") {
          this.invalidCredentials = true
          const message = `An error has occured: ${res.status} - ${res.statusText}`;
          throw new Error(message)
        }
        if(data.access == "ok") {
          this.$router.push("dashboard")
        }

        const result = {
          status: res.status + "-" + res.statusText,
          headers: {
            "Content-Type": res.headers.get("Content-Type"),
            "Content-Length": res.headers.get("Content-Length"),
          },
          data: data,
        };
        this.postResult = this.fortmatResponse(result);
      } catch (err) {
        this.postResult = err.message;
      }
    },
    clearPostOutput() {
      this.postResult = null;
    },
  },

  async mounted() {
  }
};

</script>

<style>
</style>