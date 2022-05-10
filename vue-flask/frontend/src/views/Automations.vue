<template>
  <div>
    <v-app-bar color="transparent" dark elevation="0">
      <v-img
        max-height="35"
        max-width="35"
        src="../assets/logo_simple.png"
        @click="clickLogo()"
      ></v-img>
      <v-toolbar-title class="ml-4">Automations</v-toolbar-title>

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
          <v-toolbar-title class="font-weight-bold"
            >Automations</v-toolbar-title
          >
          <v-spacer></v-spacer>

          <v-dialog v-model="dialog" full-screen>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="secondary"
                depressed
                elevation="4"
                raised
                mx-auto
                rounded
                dark
                v-bind="attrs"
                v-on="on"
              >
                <v-icon class="mr-3">mdi-plus</v-icon>Create automation
              </v-btn>
            </template>

            <v-card overflow-hidden>
              <v-card-title>
                <span class="text-h4 font-weight-bold">{{ formTitle }}</span>
              </v-card-title>
              <v-card-actions>
                <v-btn color="blue darken-1 mr-auto" text @click="save">
                  Save
                </v-btn>
                <v-btn color="blue darken-1 mr-auto" text @click="close">
                  Cancel
                </v-btn>
              </v-card-actions>

              <v-card-text>
                <v-row>
                  <v-col cols="4" md="2">
                    <h2 class="mt-12">Name</h2>
                    <v-text-field
                      v-model="AutomationName"
                      label="Insert Automation Name Here!"
                      required
                      class="mt-3 mb-6"
                    ></v-text-field>

                    <div>
                      <h2>Time</h2>
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
                          ></v-text-field>
                        </template>
                        <v-date-picker v-model="dates" range></v-date-picker>
                      </v-menu>

                      <v-menu
                        ref="menu1"
                        v-model="menuStart"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="time1"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="time1"
                            label="Start Time"
                            prepend-icon="mdi-clock-time-four-outline"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-time-picker
                          v-if="menuStart"
                          v-model="time1"
                          format="24h"
                          scrollable
                          full-width
                          @click:minute="$refs.menu1.save(time1)"
                        ></v-time-picker>
                      </v-menu>

                      <v-menu
                        ref="menu2"
                        v-model="menuEnd"
                        :close-on-content-click="false"
                        :nudge-right="40"
                        :return-value.sync="time2"
                        transition="scale-transition"
                        offset-y
                        max-width="290px"
                        min-width="290px"
                      >
                        <template v-slot:activator="{ on, attrs }">
                          <v-text-field
                            v-model="time2"
                            label="End Time"
                            prepend-icon="mdi-clock-time-four-outline"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            class="mb-6"
                          ></v-text-field>
                        </template>
                        <v-time-picker
                          v-if="menuEnd"
                          v-model="time2"
                          format="24h"
                          scrollable
                          full-width
                          @click:minute="$refs.menu2.save(time2)"
                        ></v-time-picker>
                      </v-menu>
                    </div>

                    <div>
                      <h2>Outputs</h2>
                      <v-row>
                        <v-autocomplete
                          v-model="gpiosValues"
                          :items="gpios"
                          chips
                          deletable-chips
                          multiple
                          label="Select GPIOS as outputs"
                          class="ml-3 mt-3 mb-6"
                        >
                          <template v-slot:item="{ item, on, attrs }">
                            <v-list-item v-on="on" v-bind="attrs">
                              <v-list-item-content>
                                <v-list-item-title>
                                  <v-chip dark color="primary">
                                    {{ item }}
                                  </v-chip>
                                </v-list-item-title>
                              </v-list-item-content>
                            </v-list-item>
                          </template>
                        </v-autocomplete>
                      </v-row>
                    </div>

                    <div>
                      <h2>Enable</h2>
                      <v-switch v-model="switch1"></v-switch>
                    </div>
                  </v-col>
                  <v-col md="10">
                    <ReteEditor />
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-dialog>

          <v-dialog v-model="dialogDelete" max-width="573px">
            <v-card>
              <v-card-title class="text-h5"
                >Are you sure you want to delete this automation?</v-card-title
              >
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete"
                  >Cancel</v-btn
                >
                <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                  >OK</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:[`item.state`]="{ item }">
        <v-switch
          v-model="item.state"
          hide-details
          class="ma-0 pa-0"
        ></v-switch>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>
      <template v-slot:no-data>
        <v-btn color="primary" @click="initialize"> Reset </v-btn>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import ReteEditor from "@/components/rete/ReteEditor";

export default {
  name: "AutoChips",
  components: {
    ReteEditor,
  },
  data: () => ({
    gpios: [
      "1",
      "2",
      "3",
      "4",
      "5",
      "6",
      "7",
      "8",
      "9",
      "10",
      "11",
      "12",
      "13",
      "14",
      "15",
      "16",
      "17",
      "18",
      "19",
      "20",
      "21",
      "22",
      "23",
      "24",
      "25",
      "26",
    ],
    gpiosValues: [],
    value: null,

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
        title: "Dashboard",
        icon: "mdi-view-dashboard",
        click() {
          console.log("dashboard");
          this.$router.push("dashboard");
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

    GPIOS: [
      { title: "1" },
      { title: "2" },
      { title: "3" },
      { title: "4" },
      { title: "5" },
      { title: "6" },
    ],

    time1: null,
    time2: null,
    menuStart: false,
    menuEnd: false,

    dialog: true,
    rule_dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "",
        value: "state",
        sortable: false,
        width: 0,
      },
      {
        text: "Name",
        align: "start",
        value: "name",
      },
      { text: "Rule", value: "rule" },
      { text: "GPIO Pin", value: "gpio" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    automations: [],
    editedIndex: -1,
    editedItem: {
      name: "",
      rule: 0,
      gpio: 0,
      state: false,
    },
    defaultItem: {
      name: "",
      rule: 0,
      gpio: 0,
      state: false,
    },

    editor: null,
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Automation" : "Edit Automation";
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
    this.initialize();
  },

  methods: {
    async createNodeClick() {},
    handleClick(index) {
      this.items[index].click.call(this);
    },
    clickLogo() {
      this.$router.push("dashboard");
    },

    initialize() {
      this.automations = [
        {
          name: "Automation 1",
          rule: 11,
          gpio: 6,
          state: false,
        },
        {
          name: "Automation 2",
          rule: 6,
          gpio: 9,
          state: false,
        },
        {
          name: "Automation 3",
          rule: 7,
          gpio: 16,
          state: false,
        },
        {
          name: "Automation 4",
          rule: 12,
          gpio: 12,
          state: false,
        },
        {
          name: "Automation 5",
          rule: 10,
          gpio: 16.0,
          state: false,
        },
        {
          name: "Automation 6",
          rule: 3,
          gpio: 19,
          state: false,
        },
        {
          name: "Automation 7",
          rule: 8,
          gpio: 1,
          state: false,
        },
      ];
    },

    editItem(item) {
      this.editedIndex = this.automations.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.automations.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.automations.splice(this.editedIndex, 1);
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

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.automations[this.editedIndex], this.editedItem);
      } else {
        this.automations.push(this.editedItem);
      }
      this.close();
    },
  },
};
</script>

<style>
.node-editor {
  text-align: left;
  height: 100vh;
  width: 100vw;
}
.node .control input,
.node .input-control input {
  width: 140px;
}
select,
input {
  width: 100%;
  border-radius: 30px;
  background-color: white;
  padding: 2px 6px;
  border: 1px solid #999;
  font-size: 110%;
  width: 170px;
}
</style>