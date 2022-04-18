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
          <v-dialog v-model="dialog" max-width="500px">
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
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.name"
                        label="Name"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.rule"
                        label="Rule"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.gpio"
                        label="GPIO"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-switch
                        v-model="editedItem.state"
                      ></v-switch>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">
                  Cancel
                </v-btn>
                <v-btn color="blue darken-1" text @click="save"> Save </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5"
                >Are you sure you want to delete this item?</v-card-title
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
        <v-switch v-model="item.state" hide-details class="ma-0 pa-0"></v-switch>
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
        title: "Dashboard",
        icon: "mdi-view-dashboard",
        click() {
          console.log("dashboard");
          this.$router.push("dashboard");
        },
      },
    ],

    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "",
        value: "state", sortable: false,
        width: 0
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
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
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

  created() {
    this.initialize();
  },

  methods: {
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