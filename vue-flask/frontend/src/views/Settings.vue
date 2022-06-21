<template>
  <div v-if="isLoggedIn">
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
      <v-spacer></v-spacer>

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
          <v-btn
            class="ml-4"
            :disabled="!valid"
            @click="
              submit_password();
              snackbar_password = true;
            "
          >
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
                @click="
                  submit_mqttIp
                "
              >
                submit
              </v-btn>
            </v-card-action>
          </v-col>
          <v-col cols="9" md="5" sm="6" class="mr-16">
            <v-card-subtitle class="text-h6 font-weight-medium mt-3">
              Sensors Configuration
            </v-card-subtitle>

            <v-data-table :headers="headers" :items="sensors" sort-by="sensors">
              <template v-slot:top>
                <v-toolbar flat>
                  <v-dialog v-model="dialog" max-width="500px">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        color="primary"
                        dark
                        class="mb-2"
                        v-bind="attrs"
                        v-on="on"
                        @click="resetForm"
                      >
                        New Sensor
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="text-h5">{{ formTitle }}</span>
                      </v-card-title>

                      <v-card-text>
                        <v-form ref="form" v-model="valid_sensor">
                          <v-text-field
                            v-model="editedItem.name"
                            label="Sensor name"
                            required
                            :rules="sensorRules"
                            hint="Sensor name must be the same as MQTT topic prefix"
                            persistent-hint
                          ></v-text-field>
                          <v-select
                            class="mt-3"
                            v-model="editedItem.lanes"
                            :items="lanesList"
                            label="Number of lanes"
                            solo
                            clearable
                            dense
                            required
                            :rules="sensorRules"
                          ></v-select>
                        </v-form>
                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="close">
                          Cancel
                        </v-btn>
                        <v-btn
                          color="primary"
                          text
                          @click="save"
                          :disabled="!valid_sensor"
                        >
                          Save
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card>
                      <v-card-title class="text-h5"
                        >Are you sure you want to delete this
                        item?</v-card-title
                      >
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" text @click="closeDelete"
                          >Cancel</v-btn
                        >
                        <v-btn color="primary" text @click="deleteItemConfirm"
                          >OK</v-btn
                        >
                        <v-spacer></v-spacer>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-toolbar>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="editItem(item)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
              </template>
            </v-data-table>
          </v-col>

          <v-col> </v-col>
        </v-row>
        <div class="text-center">
          <v-snackbar v-model="snackbar_password" :timeout="timeout">
            {{ text_pass }}

            <template v-slot:action="{ attrs }">
              <v-btn
                color="blue"
                text
                dense
                v-bind="attrs"
                @click="snackbar_password = false"
              >
                Close
              </v-btn>
            </template>
          </v-snackbar>
        </div>
        <div class="text-center">
          <v-snackbar v-model="snackbar_mqtt" :timeout="timeout">
            {{ text_mqtt }}

            <template v-slot:action="{ attrs }">
              <v-btn
                color="blue"
                text
                v-bind="attrs"
                @click="snackbar_mqtt = false"
              >
                Close
              </v-btn>
            </template>
          </v-snackbar>
        </div>
        <div class="text-center">
          <v-snackbar v-model="snackbar_sensors" :timeout="timeout">
            {{ text_sensors }}

            <template v-slot:action="{ attrs }">
              <v-btn
                color="blue"
                text
                v-bind="attrs"
                @click="snackbar_sensors = false"
              >
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
//import { mapGetters } from "vuex";

export default {
  data: () => ({
    //TABLE/////////////////////////////////////////////////////////////////
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Sensor",
        align: "start",
        sortable: true,
        value: "name",
      },
      { text: "Number of Lanes", align: "center", value: "lanes" },
      { text: "Actions", value: "actions", sortable: false },
    ],

    editedIndex: -1,
    editedItem: {
      id: 0,
      name: "",
      lanes: 0,
    },
    defaultItem: {
      id: 0,
      name: "",
      lanes: 0,
    },
    sensors: [],
    lanesList: [
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    ],

    sensorRules: [(v) => !!v || "Cannot be empty!"],
    text_sensors: "",
    /////////////////////////////////////////////////////////////////
    snackbar_password: false,
    snackbar_mqtt: false,
    snackbar_sensors: false,
    text_pass: "Password changed!",
    text_mqtt: "Error: Cannot communicate with System",
    text_sensors: "Number of sensors changed!",
    timeout: 4000,

    valid: true,
    valid_mqtt: true,
    valid_sensor: true,
    password: "",
    confirmPassword: "",
    passwordRules: [(v) => !!v],
    confirmPasswordRules: [(v) => !!v],

    mqttRules: [
      (v) => !!v || "Cannot be empty",
      (v) =>
        /\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b/.test(v) ||
        "Enter a valid IP address",
    ],

    broker_ip: "",

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

    async getSensors() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const responseSensors = await fetch(`http://${urlRasp}/sensors`);
      const sensors_res = await responseSensors.json();
      this.sensors = sensors_res;
    },
    resetForm() {
      this.$refs.form.reset();
    },
    editItem(item) {
      this.editedIndex = this.sensors.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.sensors.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    async deleteItemConfirm() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const id = this.editedItem.id;
      const response = await fetch(`http://${urlRasp}/sensors?id=${id}`, {
        method: "DELETE",
      });
      if (!response.ok) {
        this.text_sensors = `An error has occured: ${response.status}`;
        //this.close();
      } else {
        this.text_sensors = "Sensor Deleted!";
      }
      this.snackbar_sensors = true;
      this.sensors.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    async save() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const sensor = {
        name: this.editedItem.name,
        lanes: this.editedItem.lanes,
      };

      const file = JSON.stringify(sensor);

      if (this.editedIndex > -1) {
        
        const id = this.editedItem.id;
        const response = await fetch(`http://${urlRasp}/sensors?id=${id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: file,
        });
        Object.assign(this.sensors[this.editedIndex], this.editedItem);
        if (!response.ok) {
          this.text_sensors = `An error has occured: ${response.status}`;
          //this.close();
        } else {
          this.text_sensors = "Sensor Edited!";
        }
      } else {
        const response = await fetch(`http://${urlRasp}/sensors`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: file,
        });
        this.sensors.push(this.editedItem);
        if (!response.ok) {
          this.text_sensors = `An error has occured: ${response.status}`;
        } else {
          this.text_sensors = "Sensor Inserted! Please restart the system";
        }
      }
      this.snackbar_sensors = true;
      await this.getSensors();
      this.close();
    },

    clickLogo() {
      this.$router.push("dashboard");
    },
    handleClick(index) {
      this.items[index].click.call(this);
    },
    async submit_password() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const password = {
        password: this.confirmPassword,
      };
      const file = JSON.stringify(password);
      const response = await fetch(`http://${urlRasp}/settings`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: file,
      });
      if (!response.ok) {
        this.text_pass = `An error has occured: ${response.status}`;
      } else {
        this.text_pass = "Password changed!";
      }

      this.password = "";
      this.confirmPassword = "";
      this.$refs.myForm.reset();
    },
    async submit_mqttIp() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const broker = {
        Broker_IP: this.broker_ip,
      };
      const file = JSON.stringify(broker);
      const response = await fetch(`http://${urlRasp}/settings-broker`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: file,
      });
      if (!response.ok) {
        this.text_mqtt = `An error has occured: ${response.status}`;
      } else if (response.ok) {
        this.text_mqtt = "Broker IP changed! Please restart the system!";
      }

      this.snackbar_mqtt = true;
    },

    async getBrokerIP() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const response = await fetch(`http://${urlRasp}/settings-broker`);
      const ip = await response.json();
      this.broker_ip = ip.Broker;
    },
  },

  computed: {
    ...mapGetters(["isLoggedIn"]),
    formTitle() {
      return this.editedIndex === -1 ? "New Sensor" : "Edit Sensor";
    },
    passwordConfirmationRule() {
      return () =>
        this.password === this.confirmPassword || "Password must match";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },
};
</script>

<style>
</style>