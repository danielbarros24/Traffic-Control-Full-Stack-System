<template>
  <div>
    <v-app-bar color="transparent" dark elevation="0">
      <v-img
        max-height="35"
        max-width="35"
        src="../assets/logo_simple.png"
        @click="clickLogo()"
      ></v-img>
      <v-toolbar-title class="ml-4">Settings</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-menu transition="slide-y-transition" offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            v-for="(item, index) in items"
            :key="index"
            @click="handleClick(index)"
          >
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-card>
      <v-card-title class="text-h4 font-weight-bold">
        Administrator
      </v-card-title>
      <v-space></v-space>

      <div class="ml-3">
        <v-card-subtitle class="text-h6 font-weight-medium">
          Change Password
        </v-card-subtitle>

        <v-card-text>
          <v-form v-model="valid">
            <v-row>
              <v-col cols="5" md="2">
                <v-text-field
                  v-model="firstname"
                  :rules="nameRules"
                  label="Set new password"
                  required
                ></v-text-field>
              </v-col>

              <v-col cols="5" md="2">
                <v-text-field
                  v-model="lastname"
                  :rules="nameRules"
                  label="Confirm new password"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-action>
          <v-btn class="ml-4" @click="submit_password"> submit </v-btn>
        </v-card-action>

        <v-row class="mt-8">
          <v-col cols="9" md="5" sm="6" class="mr-16">
            <v-card-subtitle class="text-h6 font-weight-medium">
              MQTT Broker Configuration
            </v-card-subtitle>

            <v-card-text> 
              <p class="text-h6 font-weight-medium mt-8">
                Change MQTT Broker IP
              </p>
              <v-form>
                <v-text-field label="Set new broker IP" required value="192.168.1.169"></v-text-field>
              </v-form>
            </v-card-text>

            <v-card-action>
              <v-btn class="ml-4 mb-6" @click="submit_mqttIp"> submit </v-btn>
            </v-card-action>
          </v-col>
            <v-card-subtitle class="text-h6 font-weight-medium mt-3">
              Sensors Configuration
            </v-card-subtitle>
          <v-col>

          </v-col>
        </v-row>
      </div>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    items: [
      {
        title: "Logout",
        icon: "mdi-logout",
        click() {
          console.log("logout");
          this.$router.push("/");
        },
      },
      {
        title: "Automations",
        icon: "mdi-auto-fix",
        click() {
          console.log("automations");
          this.$router.push("automations");
        },
      },
      {
        title: "Settings",
        icon: "mdi-cogs",
        click() {
          console.log("settings");
          this.$router.push("settings");
        },
      },
    ],
  }),

  methods: {
    clickLogo() {
      this.$router.push("dashboard");
    },
    handleClick(index) {
      this.items[index].click.call(this);
    },
    submit_password() {
      this.$v.$touch();
    },
    submit_mqttIp() {
      this.$v.$touch();
    },
  },
};
</script>

<style>
</style>