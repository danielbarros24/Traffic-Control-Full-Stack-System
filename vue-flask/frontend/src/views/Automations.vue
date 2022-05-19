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
          <v-btn
            color="secondary"
            depressed
            elevation="4"
            raised
            mx-auto
            rounded
            dark
            @click="createItem"
          >
            <v-icon class="mr-3">mdi-plus</v-icon>Create automation
          </v-btn>
          <v-dialog v-model="dialog" full-screen>
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
                      v-model="editedItem.name"
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
                          ></v-text-field>
                        </template>
                        <v-time-picker
                          v-if="menuStart"
                          v-model="editedItem.startHour"
                          format="24h"
                          scrollable
                          full-width
                          @click:minute="$refs.menu1.save(editedItem.startHour)"
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
                      <h2>Outputs</h2>
                      <v-row>
                        <v-autocomplete
                          v-model="editedItem.gpios"
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
                                    {{ item.text }}
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
                      <v-switch v-model="editedItem.enable"></v-switch>
                    </div>

                    <v-btn @click="onExport">Export</v-btn>

                    <v-textarea v-model="editorJSON"></v-textarea>
                    <v-btn @click="onEditorSync">Sync</v-btn>
                    <v-btn @click="onEditorImport">Import</v-btn>
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
      <template v-slot:[`item.enable`]="{ item }">
        <v-switch
          :input-value="item.enable"
          @change="updateEnable($event, item)"
          hide-details
          class="ma-0 pa-0"
        ></v-switch>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import ReteEditor from "@/components/rete/ReteEditor";
import * as dayjs from 'dayjs'


export default {
  name: "Automations",
  components: {
    ReteEditor,
  },

  data() {
    const gpios = [];
    for (let i = 1; i < 27; i++) {
      gpios.push({
        text: `GPIO ${i}`,
        value: i,
      });
    }

    return {
      gpios: gpios,
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

      menuStart: false,
      menuEnd: false,
      menu1: null,
      menu2: null,

      switch1: false,

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
        { text: "Actions", value: "actions", sortable: false },
      ],
      automations: [],
      editedIndex: -1,
      editedItem: {
        id: 0,
        name: "",
        rule: 0,
        gpios: [],
        enable: false,
        dates: [],
        startHour: "",
        endHour: "",
        blueprint: {},
      },

      defaultItem: {
        id: 0,
        name: "",
        rule: 0,
        gpios: [],
        enable: false,
        dates: [],
        startHour: "",
        endHour: "",
        blueprint: {},
      },

      editor: null,
      editorJSON: "",
    };
  },

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Automation" : "Edit Automation";
    },
    dateRangeText() {
      return this.editedItem.dates.join(" ~ ");
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
    const response = await fetch("http://127.0.0.1:5000/automation");
    const json = await response.json();
    this.automations = json.map((val) => {
      const startTime = new Date(val.startTime);
      const endTime = new Date(val.endTime);

      delete val.startTime;
      delete val.endTime;

      val.dates = [
        `${dayjs(startTime).format('YYYY')}-${
          dayjs(startTime).format('MM')
        }-${dayjs(startTime).format('DD')}`,
        `${dayjs(endTime).format('YYYY')}-${
          dayjs(endTime).format('MM')
        }-${dayjs(endTime).format('DD')}`,
      ];
      val.startHour = `${dayjs(startTime).format('HH')}:${dayjs(startTime).format('mm')}`;
      val.endHour = `${dayjs(endTime).format('HH')}:${dayjs(endTime).format('mm')}`;

      return val;
    });
    
  },

  methods: {
    async createNodeClick() {},
    handleClick(index) {
      this.items[index].click.call(this);
    },
    clickLogo() {
      this.$router.push("dashboard");
    },

    async editItem(item) {
      this.editedIndex = this.automations.indexOf(item);
      this.editedItem = Object.assign({}, item);

      this.dialog = true;

      setTimeout(async () => {
        const blueprint = this.editedItem.blueprint;
        // import blueprint
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
      const id = this.editedItem.id;
      await fetch(`http://127.0.0.1:5000/automation?id=${id}`, {
        method: "DELETE",
      });
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

    async save() {
      const editor = this.editor;

      const blueprint = await editor.toJSON();

      const endNode = this.editor.nodes.find((node) => node.name === "End");
      const endComponent = editor.getComponent("End");

      const logic = endComponent.toJsonLogic?.(endNode);

      const dates = this.editedItem.dates;

      const startHour = this.editedItem.startHour;
      const endHour = this.editedItem.endHour;

      const startTime = dates[0] + "T" + startHour + ":00.000Z";
      const endTime = dates[1] + "T" + endHour + ":00.000Z";

      const automation = {
        name: this.editedItem.name,
        startTime: startTime,
        endTime: endTime,
        enable: this.editedItem.enable,
        gpios: this.editedItem.gpios,
        rules: logic,
        blueprint: blueprint,
      };

      const file = JSON.stringify(automation);

      console.log(file);

      if (this.editedIndex > -1) {
        const id = this.editedItem.id;
        await fetch(`http://127.0.0.1:5000/automation?id=${id}`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: file,
        });
        Object.assign(this.automations[this.editedIndex], this.editedItem);
      } else {
        await fetch("http://127.0.0.1:5000/automation", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: file,
        });
        this.automations.push(this.editedItem);
      }

      this.close();
    },

    async updateEnable(event, item) {
      const id = item.id;

      await fetch(`http://127.0.0.1:5000/automation?id=${id}`, {
      method: "PATCH",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        enable: !!event
      })
    });
      
    },

    async onExport() {
      const editor = this.editor;

      const endNode = this.editor.nodes.find((node) => node.name === "End");
      const endComponent = editor.getComponent("End");

      console.log(JSON.stringify(endComponent.toJsonLogic?.(endNode)));
    },

    async onEditorImport() {
      await this.editor.fromJSON(JSON.parse(this.editorJSON));
    },

    async onEditorSync() {
      this.editorJSON = JSON.stringify(await this.editor.toJSON());
    },
  },
};
</script>
