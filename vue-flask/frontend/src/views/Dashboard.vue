<template>
  <div>
      <v-app-bar color="transparent" dark elevation="0">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title>Dashboard</v-toolbar-title>

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
    <v-row no-gutters>
      <v-col cols="1" sm="3" md="2">
        <v-card
          class="d-flex ml-5 mt-13 pa-6"
          min-width="290"
          elevation="20"
          outlined
        >
          <v-card-text>
            <h2 class="text-h6 text--primary">Location</h2>
            <v-radio-group v-model="Location" mandatory>
              <v-radio
                label="Camera 1"
                value="cam-1"
                color="primary"
              ></v-radio>
              <v-radio
                label="Camera 2"
                value="cam-2"
                color="primary"
              ></v-radio>
            </v-radio-group>

            <div class="my-12">
              <h2 class="text-h6 text--primary">Time</h2>

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
                  clearable
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="dates"
                range
              ></v-date-picker>
            </v-menu>
            </div>
            

            <h2 class="text-h6 text--primary">Indicators</h2>
            <v-checkbox
              v-on:click="VehicleCountsGraph = !VehicleCountsGraph"
              label="Vehicle Counts"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-on:click="NumberOfStayGraph = !NumberOfStayGraph"
              label="Number of Stay"
              value="counts"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-on:click="LenghtOfStayGraph = !LenghtOfStayGraph"
              label="Lenght of Stay"
              value="counts"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-on:click="TrafficFlowAnalysisGraph = !TrafficFlowAnalysisGraph"
              label="Traffic flow"
              value="counts"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-on:click="PedestrianFlowGraph = !PedestrianFlowGraph"
              label="Pedestrian Flow"
              value="counts"
              hide-details
            ></v-checkbox>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="6" md="10" no-gutters class="mt-13">
        <v-row :align="align" no-gutters max-height="320">
          <v-expand-transition>
            <v-card
              class="d-flex ml-3 mb-6 pa-6"
              width="1000"
              min-height="320"
              outlined
              v-if="VehicleCountsGraph"
            >
              <v-card-title class="text-center">Vehicle Counts</v-card-title>
            </v-card>
          </v-expand-transition>
          <v-expand-transition>
            <v-card
              class="d-flex ml-3 mb-6 pa-6"
              width="400"
              min-height="320"
              outlined
              v-if="TrafficFlowAnalysisGraph"
            >
              <v-card-title class="text-center"
                >Traffic Flow analysis</v-card-title
              >
            </v-card>
          </v-expand-transition>
        </v-row>

        <v-row :align="align" no-gutters max-height="320">
          <v-expand-transition>
            <v-card
              class="d-flex ml-3 pa-6"
              min-width="400"
              width="100"
              height="320"
              outlined
              v-if="NumberOfStayGraph"
            >
              <v-card-title class="text-center">Number of Stay</v-card-title>
            </v-card>
          </v-expand-transition>

          <v-expand-transition>
            <v-card
              class="d-flex ml-3 pa-6"
              min-width="400"
              width="700"
              height="320"
              outlined
              v-if="PedestrianFlowGraph"
            >
              <v-card-title class="text-center">Pedestrian Flow</v-card-title>
            </v-card>
          </v-expand-transition>

          <v-expand-transition>
            <v-card
              class="d-flex ml-3 pa-6"
              min-width="400"
              width="200"
              height="320"
              outlined
              v-if="LenghtOfStayGraph"
            >
              <v-card-title class="text-center">Lenght of Stay</v-card-title>
            </v-card>
          </v-expand-transition>
        </v-row>
      </v-col>
    </v-row>
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
        title: "Settings",
        icon: "mdi-cogs",
        click() {
          console.log("settings");
          this.$router.push("settings");
        },
      },
    ],

    dates: [],

    VehicleCountsGraph: false,
    TrafficFlowAnalysisGraph: false,
    NumberOfStayGraph: false,
    PedestrianFlowGraph: false,
    LenghtOfStayGraph: false,
  }),

  methods: {
    handleClick(index) {
      this.items[index].click.call(this);
    },
  },
  computed: {
      dateRangeText () {
        return this.dates.join(' ~ ')
      },
    },
};
</script>
