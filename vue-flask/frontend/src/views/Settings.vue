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
          <v-form v-model="valid" ref="myForm">
            <v-row>
              <v-col cols="5" md="2">
                <v-text-field
                  v-model="password"
                  type="password"
                  :rules="passwordRules"
                  label="Set new password"
                ></v-text-field>
              </v-col>

              <v-col cols="5" md="2">
                <v-text-field
                  v-model="confirmPassword"
                  type="password"
                  :rules="confirmPasswordRules.concat(passwordConfirmationRule)"
                  label="Confirm new password"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
        <v-card-action>
          <v-btn class="ml-4" :disabled="!valid" @click="submit_password(); snackbar_password = true;">
            submit
          </v-btn>
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
              <v-form v-model="valid_mqtt">
                <v-text-field
                  v-model="broker_ip"
                  label="Set new broker IP"
                  required
                  :rules="mqttRules"
                ></v-text-field>
              </v-form>
            </v-card-text>

            <v-card-action>
              <v-btn
                class="ml-4 mb-6"
                :disabled="!valid_mqtt"
                @click="submit_mqttIp();snackbar_mqtt = true;"
              >
                submit
              </v-btn>
            </v-card-action>
          </v-col>
          <v-col cols="9" md="5" sm="6" class="mr-16">
            <v-card-subtitle class="text-h6 font-weight-medium mt-3">
              Sensors Configuration
            </v-card-subtitle>

            <v-card-text class="ma">
              <p class="text-h6 font-weight-medium mt-8">
                Change sensors number
              </p>
              <v-form v-model="valid_sensors">
                <v-text-field
                  v-model="n_sensors"
                  label="Enter new number of sensors"
                  required
                  :rules="SensorsRules"
                ></v-text-field>
              </v-form>
            </v-card-text>

            <v-card-action>
              <v-btn
                class="ml-4 mb-6"
                :disabled="!valid_sensors"
                @click="submit_sensors();snackbar_sensors = true;"
              >
                submit
              </v-btn>
            </v-card-action>
          </v-col>

          <v-col> </v-col>
        </v-row>
        <div class="text-center">
          <v-snackbar v-model="snackbar_password" :timeout="timeout">
            {{ text_pass }}

            <template v-slot:action="{ attrs }">
              <v-btn color="blue" text v-bind="attrs" @click="snackbar_password = false">
                Close
              </v-btn>
            </template>
          </v-snackbar>
        </div>
        <div class="text-center">
          <v-snackbar v-model="snackbar_mqtt" :timeout="timeout">
            {{ text_mqtt }}

            <template v-slot:action="{ attrs }">
              <v-btn color="blue" text v-bind="attrs" @click="snackbar_mqtt = false">
                Close
              </v-btn>
            </template>
          </v-snackbar>
        </div>
        <div class="text-center">
          <v-snackbar v-model="snackbar_sensors" :timeout="timeout">
            {{ text_sensors }}

            <template v-slot:action="{ attrs }">
              <v-btn color="blue" text v-bind="attrs" @click="snackbar_sensors = false">
                Close
              </v-btn>
            </template>
          </v-snackbar>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
import { consoleError } from 'vuetify/lib/util/console';

export default {
  data: () => ({
    snackbar_password: false,
    snackbar_mqtt: false,
    snackbar_sensors: false,
    text_pass: "Password changed!",
    text_mqtt: "Broker IP changed! Please restart the system!",
    text_sensors: "Number of sensors changed!",
    timeout: 4000,

    valid: true,
    valid_mqtt: true,
    password: "",
    confirmPassword: "",
    passwordRules: [(v) => !!v],
    confirmPasswordRules: [(v) => !!v],

    mqttRules: [
      v => !!v || "Cannot be empty",
      v =>  /\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b/.test(v) || 'Enter a valid IP address',],

    broker_ip: "",

    valid_sensors: true,
    n_sensors: "1" ,
    SensorsRules: [(v) => !!v || "Cannot be empty"],

    items: [
      {
        title: "Logout",
        icon: "mdi-logout",
        click() {
          this.$router.push("/");
        },
      },
      {
        title: "Dashboard",
        icon: "mdi-view-dashboard",
        click() {
          this.$router.push("dashboard");
        },
      },
      {
        title: "Processes",
        icon: "mdi-auto-fix",
        click() {
          this.$router.push("processes");
        },
      },
      
    ],
  }),

  async mounted() {
    await this.getSensors();
    await this.getBrokerIP();
  },

  methods: {
    clickLogo() {
      this.$router.push("dashboard");
    },
    handleClick(index) {
      this.items[index].click.call(this);
    },
    async submit_password() {
      const password = {
        password: this.confirmPassword
      }
      const file = JSON.stringify(password);
      const response = await fetch(`http://127.0.0.1:5000/settings`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: file,
      });
      if (!response.ok) {
          this.text_pass = `An error has occured: ${response.status}`
        }
      else {
        this.text_pass = "Password changed!"
      }

      this.password = ""
      this.confirmPassword = ""
      this.$refs.myForm.reset();
      
    },
    async submit_mqttIp() {
      const broker = {
        Broker_IP: this.broker_ip
      }
      const file = JSON.stringify(broker);
      const response = await fetch(`http://127.0.0.1:5000/settings-broker`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: file,
      });

      if (!response.ok) {
          this.text_mqtt = `An error has occured: ${response.status}`
        }
      else {
        this.text_mqtt = "Broker IP changed! Please restart the system!"
      }
    },

    async submit_sensors() {
      const sensor = {
        Sensors: this.n_sensors
      }
      const file = JSON.stringify(sensor);
      const response = await fetch(`http://127.0.0.1:5000/settings-sensors`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: file,
      });

      if (!response.ok) {
          this.text_mqtt = `An error has occured: ${response.status}`
        }
      else {
        this.text_mqtt = "Broker IP changed! Please restart the system!"
      }

    },
    async getBrokerIP() {
      const response = await fetch("http://127.0.0.1:5000/settings-broker");
      const ip= await response.json();
      this.broker_ip = ip.Broker;
    },

    async getSensors() {
      const response = await fetch("http://127.0.0.1:5000/settings-sensors");
      const number = await response.json();
      this.n_sensors = number.Number;
      
    },
  },

  computed: {
    passwordConfirmationRule() {
      return () =>
        this.password === this.confirmPassword || "Password must match";
    },
  },
};
</script>

<style>
</style>