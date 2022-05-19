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
                      <v-btn @click="postData()" rounded color="deep-purple darken-3" class="mt-4" block dark 
                      >SIGN IN</v-btn
                    >
                    <v-text-field v-show="login" color="red">
                      data
                    </v-text-field>
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
    login: false
  }),
  props: {
    source: String,
  },

  methods:{
    async postData() {
      const postData = {
        username: this.username,
        password: this.password,
      }
      try {
        const res = await fetch("http://127.0.0.1:5000/login", {
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