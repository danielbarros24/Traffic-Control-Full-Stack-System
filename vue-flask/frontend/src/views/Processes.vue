<template>
  <div>
    <v-app-bar color="transparent" dark elevation="0">
      <v-img
        max-height="35"
        max-width="35"
        src="../assets/logo_simple.png"
        @click="clickLogo()"
      ></v-img>
      <v-toolbar-title class="ml-4">Processes</v-toolbar-title>

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

    <v-data-table
      :headers="headers"
      :items="automations"
      class="elevation-24 mt-13"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title class="font-weight-bold">Processes</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            depressed
            elevation="4"
            raised
            mx-auto
            rounded
            dark
            @click="createProcess"
          >
            <v-icon class="mr-3">mdi-plus</v-icon>Create process
          </v-btn>
          <v-dialog v-model="dialog" full-screen>
            <v-card overflow-hidden>
              <v-card-title>
                <span class="text-h4 font-weight-bold">{{ formTitle }}</span>
              </v-card-title>
              <v-card-actions>
                <v-btn
                  color="primary"
                  text
                  :disabled="!(all_valid & valid)"
                  @click="save"
                >
                  Save
                </v-btn>
                <v-btn color="primary" text @click="close"> Cancel </v-btn>
              </v-card-actions>
              <v-card-text>
                <v-row>
                  <v-col>
                    <v-form ref="form" v-model="valid">
                      <h2 class="mt-12">Name</h2>
                      <v-text-field
                        v-model="editedItem.name"
                        label="Insert process Name Here!"
                        class="mt-3 mb-6"
                        :rules="nameRules"
                        required
                      ></v-text-field>

                      <div>
                        <h2 class="mt-12">Time</h2>
                        <v-menu
                          v-model="menu2"
                          :close-on-content-click="false"
                          :nudge-right="40"
                          transition="scale-transition"
                          offset-y
                          min-width="auto"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="dateRangeText"
                              label="Select date range"
                              prepend-icon="mdi-calendar"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                              class="mt-3"
                              required
                              :rules="dateRules"
                            ></v-text-field>
                          </template>
                          <v-date-picker
                            v-model="editedItem.dates"
                            range
                          ></v-date-picker>
                        </v-menu>

                        <v-menu
                          ref="menu1"
                          v-model="menuStart"
                          :close-on-content-click="false"
                          :nudge-right="40"
                          :return-value.sync="editedItem.startHour"
                          transition="scale-transition"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="editedItem.startHour"
                              label="Start Time"
                              prepend-icon="mdi-clock-time-four-outline"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                              :rules="nameRules"
                              required
                            ></v-text-field>
                          </template>
                          <v-time-picker
                            v-if="menuStart"
                            v-model="editedItem.startHour"
                            format="24h"
                            scrollable
                            full-width
                            @click:minute="
                              $refs.menu1.save(editedItem.startHour)
                            "
                          ></v-time-picker>
                        </v-menu>

                        <v-menu
                          ref="menu2"
                          v-model="menuEnd"
                          :close-on-content-click="false"
                          :nudge-right="40"
                          :return-value.sync="editedItem.endHour"
                          transition="scale-transition"
                          offset-y
                          max-width="290px"
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="editedItem.endHour"
                              label="End Time"
                              prepend-icon="mdi-clock-time-four-outline"
                              readonly
                              v-bind="attrs"
                              v-on="on"
                              class="mb-6"
                              :rules="nameRules"
                              required
                            ></v-text-field>
                          </template>
                          <v-time-picker
                            v-if="menuEnd"
                            v-model="editedItem.endHour"
                            format="24h"
                            scrollable
                            full-width
                            @click:minute="$refs.menu2.save(editedItem.endHour)"
                          ></v-time-picker>
                        </v-menu>
                      </div>
                      <div>
                        <h2 class="mt-12">Enable</h2>
                        <v-switch
                          color="primary"
                          v-model="editedItem.enable"
                        ></v-switch>
                      </div>

                      <v-btn class="mt-12" @click="Validate" :disabled="!valid"
                        >Validate Rule</v-btn
                      >
                    </v-form>
                  </v-col>

                  <v-col md="10">
                    <ReteEditor v-model="editor" />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-dialog>

          <v-dialog v-model="dialogDelete" max-width="573px">
            <v-card>
              <v-card-title class="text-h5"
                >Are you sure you want to delete this processs?</v-card-title
              >
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="closeDelete">Cancel</v-btn>
                <v-btn
                  color="primary"
                  text
                  @click="
                    deleteItemConfirm();
                    snackbar_deleted = true;
                  "
                  >OK</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:[`item.enable`]="{ item }">
        <v-switch
          :input-value="item.enable"
          @change="updateEnable($event, item)"
          hide-details
          class="ma-0 pa-0"
          color="primary"
        ></v-switch>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>
    </v-data-table>
    <div class="text-center">
      <v-snackbar v-model="snackbar_saved" :timeout="timeout">
        {{ process_save }}

        <template v-slot:action="{ attrs }">
          <v-btn
            color="blue"
            text
            v-bind="attrs"
            @click="snackbar_saved = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>
    <div class="text-center">
      <v-snackbar v-model="snackbar_deleted" :timeout="timeout">
        {{ process_delete }}

        <template v-slot:action="{ attrs }">
          <v-btn
            color="blue"
            text
            v-bind="attrs"
            @click="snackbar_deleted = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>
    <v-spacer></v-spacer>
    <div class="text-center">
      <v-snackbar
        v-for="(snackbar, index) in snackbars.filter((s) => s.showing)"
        :key="snackbar.text"
        v-model="snackbar.showing"
        :timeout="0"
        elevation="24"
        :color="snackbar.color"
        :style="`bottom: ${index * 60 + 8}px`"
      >
        <h2 class="font-weight-medium">{{ snackbar.text }}</h2>

        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="snackbar.showing = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>

    <div class="text-center">
      <v-snackbar v-model="brokerFail" color="red" >
        <h2 class="font-weight-medium">BROKER COMMUNICATION DOWN!</h2>

        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="brokerFail = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </div>
  </div>
</template>

<script>

import ReteEditor from "@/components/rete/ReteEditor";
import * as dayjs from "dayjs";
import { mapState } from "vuex";
import { mapGetters } from 'vuex'

export default {
  name: "Processes",
  components: {
    ReteEditor,
  },

  data() {
    return {
      brokerFail: false,
      gpios: [],
      value: null,

      items: [
        {
          title: "Logout",
          icon: "mdi-logout",
          click() {
            this.$store.dispatch('logout');
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
          title: "Settings",
          icon: "mdi-cogs",
          click() {
            this.$router.push("settings");
          },
        },
      ],

      nameRules: [(v) => !!v],
      dateRules: [
        (v) => !!v || "Insert 2 dates",
        (v) =>
          /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])~\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/.test(
            v
          ) || "Insert 2 dates!",
      ],

      valid: true,
      all_valid: false,

      process_save: "Process Saved!",
      process_delete: "Process Deleted!",

      //snackbar: false,
      textProcessTrigger: "",

      snackbar_saved: false,
      snackbar_deleted: false,
      timeout: 4000,

      menuStart: false,
      menuEnd: false,
      menu1: null,
      menu2: null,

      switch1: true,

      AutomationName: "",
      dialog: false,
      rule_dialog: false,
      dialogDelete: false,

      headers: [
        {
          text: "",
          value: "enable",
          sortable: false,
          width: 0,
        },
        {
          text: "Name",
          align: "start",
          value: "name",
        },
        {
          text: "Triggering",
          align: "center",
          value: "triggering",
        },
        {
          text: "Last Trigger",
          align: "center",
          value: "lastTimeTriggerDisplay",
        },
        { text: "Actions", value: "actions", sortable: false },
      ],
      automations: [],
      editedIndex: -1,
      editedItem: {
        id: 0,
        name: "",
        rule: 0,
        enable: true,
        dates: [],
        startHour: "",
        endHour: "",
        triggering: false,
        lastTimeTrigger: "",
        lastTimeTriggerDisplay: "Never",
        notification: false,
        blueprint: {},
      },

      defaultItem: {
        id: 0,
        name: "",
        rule: 0,
        enable: true,
        dates: [],
        startHour: "",
        endHour: "",
        triggering: false,
        lastTimeTrigger: "",
        lastTimeTriggerDisplay: "Never",
        notification: false,
        blueprint: {},
      },

      editor: null,
      editorJSON: "",
    };
  },

  computed: {
    ...mapState(["snackbars"]),
    ...mapGetters('auth', {
				isAuth: 'isAuthenticated',
			}),
    formTitle() {
      return this.editedIndex === -1 ? "New Process" : "Edit Processes";
    },
    dateRangeText() {
      return this.editedItem.dates.join("~");
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

  async mounted() {
    const urlDesktop = "127.0.0.1:5000"
    const urlRasp = "192.168.1.216:5000"
    
    await this.getProcesses();
    await this.getPins();
    this.interval = setInterval(() => this.loopFunction(), 3000);
  },

  async beforeDestroy() {
    clearInterval(this.interval)
  },

  methods: {
    async loopFunction() {
      await this.getProcesses()
      await this.getBrokerState()
    },
    async getBrokerState() {
      const urlDesktop = "127.0.0.1:5000";
      const urlRasp = "192.168.1.216:5000";

      const responseState= await fetch(`http://${urlRasp}/broker-state`, {headers: {
        'Authorization': `Bearer ${localStorage.getItem("token")}`
      }});
      const res = await responseState.json();

      if (res.state == "ok") {
        this.brokerFail = false
      }
      else {
        this.brokerFail = true
      }
    },
    notificationTest() {
      this.$store.dispatch("setSnackbar", {
        text: `process triggered!`,
      });
    },

    async getProcesses() {
      
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const responseAutomations = await fetch(`http://${urlRasp}/process`, {headers: {
        'Authorization': `Bearer ${localStorage.getItem("token")}`
      }});

      const jsonAutomations = await responseAutomations.json();

      this.automations = jsonAutomations.map((val) => {
        const startTime = new Date(val.startTime);
        const endTime = new Date(val.endTime);
        const triggering = val.triggering;
        const notification = val.notification;
        const processName = val.name;

        if (dayjs(val.lastTimeTrigger).isValid()) {
          
          val.lastTimeTriggerDisplay = dayjs(val.lastTimeTrigger).fromNow();
          
        } else {
          val.lastTimeTriggerDisplay = "Never";
        }

        if (notification) {
          this.$store.dispatch("setSnackbar", {
            text: `${processName} process triggered!`,
          });
        }

        delete val.notification;
        delete val.startTime;
        delete val.endTime;
        delete val.triggering;

        val.dates = [
          `${dayjs(startTime).format("YYYY-MM-DD")}`,
          `${dayjs(endTime).format("YYYY-MM-DD")}`,
        ];
        val.startHour = `${dayjs(startTime).format("HH:mm")}`;
        val.endHour = `${dayjs(endTime).format("HH:mm")}`;
        val.triggering = triggering;

        return val;
      });
    },

    createProcess() {
      this.createItem();
      this.getPins();
      this.$refs.form.reset();
    },

    triggerSavedProcess() {
      this.snackbar_saved = true;
    },

    triggerDeletedProcess() {
      this.snackbar_deleted = true;
    },

    handleClick(index) {
      this.items[index].click.call(this);
    },

    clickLogo() {
      this.$router.push("dashboard");
    },

    async getPins() {

      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const responseGpios = await fetch(`http://${urlRasp}/pins`, {headers: {
        'Authorization': `Bearer ${localStorage.getItem("token")}`
      }});
      const jsonGpios = await responseGpios.json();

      this.gpios = jsonGpios.map((value) => ({
        text: `GPIO ${value}`,
        value: value,
      }));
    },

    async editItem(item) {
      this.editedIndex = this.automations.indexOf(item);
      this.editedItem = Object.assign({}, item);

      this.dialog = true;

      setTimeout(async () => {
        const blueprint = this.editedItem.blueprint;
        await this.editor.fromJSON(blueprint);
      }, 200);
    },

    async createItem() {
      this.dialog = true;
      setTimeout(async () => {
        await this.editor.clear();
      }, 200);
    },

    deleteItem(item) {
      this.editedIndex = this.automations.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    async deleteItemConfirm() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"
      
      const id = this.editedItem.id;
      const response = await fetch(`http://${urlRasp}/process?id=${id}`, {
        method: "DELETE",
        headers: { 'Authorization': `Bearer ${localStorage.getItem("token")}` }
      });
      if (!response.ok) {
        this.process_delete = `An error has occured: ${response.status}`;
      } else {
        this.process_delete = "Process Deleted!";
      }
      this.automations.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
      this.all_valid = false;
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });

      this.all_valid = false;
    },

    async save() {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const editor = this.editor;

      const blueprint = await editor.toJSON();

      const endNode = this.editor.nodes.find((node) => node.name === "GPIO");
      const endComponent = editor.getComponent("GPIO");

      const gpios = this.editor.nodes
        .filter((node) => node.name === "GPIO")
        .map((node) => this.editor.getComponent(node.name).toGPIO(node));

      const logic = endComponent.toJsonLogic?.(endNode);

      const dates = this.editedItem.dates;

      const startHour = this.editedItem.startHour;
      const endHour = this.editedItem.endHour;

      const startTime = dayjs(dates[0] + " " + startHour).toISOString();
      const endTime = dayjs(dates[1] + " " + endHour).toISOString();

      const automation = {
        name: this.editedItem.name,
        startTime: startTime,
        endTime: endTime,
        enable: this.editedItem.enable,
        gpios: gpios,
        triggering: false,
        lastTimeTrigger: "",
        notification: false,
        rules: logic,
        blueprint: blueprint,
      };

      const file = JSON.stringify(automation);
      console.log(file);

      if (this.editedIndex > -1) {

        const id = this.editedItem.id;
        const response = await fetch(`http://${urlRasp}/process?id=${id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json", 'Authorization': `Bearer ${localStorage.getItem("token")}` },
          body: file,
        });
        Object.assign(this.automations[this.editedIndex], this.editedItem);

        if (!response.ok) {
          this.process_save = `An error has occured: ${response.status}`;
          this.close();
        } else {
          this.process_save = "Process Edited!";
        }
      } else {
        const response = await fetch(`http://${urlRasp}/process`, {
          method: "POST",
          headers: { "Content-Type": "application/json", 'Authorization': `Bearer ${localStorage.getItem("token")}` },
          body: file,
        });
        this.automations.push(this.editedItem);
        if (!response.ok) {
          this.process_save = `An error has occured: ${response.status}`;
          this.close();
        } else {
          this.process_save = "Process Saved!";
        }
      }
      this.close();
      this.triggerSavedProcess();
    },

    async updateEnable(event, item) {
      const urlDesktop = "127.0.0.1:5000"
      const urlRasp = "192.168.1.216:5000"

      const id = item.id;

      await fetch(`http://${urlRasp}/process?id=${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json", 'Authorization': `Bearer ${localStorage.getItem("token")}` },
        body: JSON.stringify({
          enable: !!event,
          triggering: false
        }),
      });
    },

    async Validate() {
      const endNodes = this.editor.nodes.filter((node) => node.name === "GPIO");

      if (endNodes.length <= 0) {
        this.all_valid = false;
        return;
      }

      const inputNum0 = endNodes[0].inputs.get("num");

      if (inputNum0.connections.length == 0) {
        this.all_valid = false;
        return;
      }

      const connection0 = inputNum0.connections[0];
      const connectionNode0 = connection0.output.node;
      const connectionComponent0 = this.editor.getComponent(
        connectionNode0.name
      );

      for (let i = 1; i < endNodes.length; i++) {
        const inputNum = endNodes[i].inputs.get("num");
        const { connections } = inputNum;

        if (connections.length == 0) {
          this.all_valid = false;
          return;
        }

        const connection = connections[0];
        const connectionNode = connection.output.node;
        const connectionComponent = this.editor.getComponent(
          connectionNode.name
        );

        if (connectionComponent0 !== connectionComponent) {
          this.all_valid = false;
          return;
        }
      }
      this.all_valid = true;
    },
  },
};
</script>
