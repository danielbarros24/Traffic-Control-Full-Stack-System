<template>
  <div v-if="isLoggedIn">
    <v-app-bar color="transparent" dark elevation="0">
      <v-img
        max-height="35"
        max-width="35"
        src="../assets/logo_simple.png"
      ></v-img>
      <v-toolbar-title class="ml-4">Dashboard</v-toolbar-title>

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
            <h2 class="text-h6 text--primary">Sensors</h2>
            <v-radio-group v-model="radioGroup" mandatory>
              <v-radio
                v-for="sensor in sensors"
                :key="sensor"
                :label="`${sensor.name}`"
                :value="sensor.name"
              ></v-radio>
            </v-radio-group>

            <div class="my-5">
              <v-form ref="form" v-model="valid">
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
                      v-bind="attrs"
                      v-on="on"
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
              </v-form>
            </div>

            <h2 class="text-h6 text--primary">Indicators</h2>
            <v-checkbox
              v-model="carCountChart"
              label="Car Flow"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="truckCountChart"
              label="Truck Flow"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="bikeCountChart"
              label="Bike flow"
              hide-details
            ></v-checkbox>
            <v-checkbox
              v-model="doubleParkVehicles"
              label="Double Park Vehicles"
              hide-details
            ></v-checkbox>
            <v-btn
              depressed
              color="primary"
              class="d-flex mt-10"
              @click="submitGetData"
              :disabled="!valid"
            >
              Submit
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="6" md="10" no-gutters class="mt-13">
        <v-row no-gutters max-height="800">
          <v-card
            class="d-flex mb-4 pt-1 ml-3 px-5"
            width="750"
            height="380"
            outlined
          >
          <v-col>
            <h1 class="d-flex justify-center mb-3 font-weight-regular">Car Flow</h1>
            <area-chart
              :data="dataCountCar"
              :colors="['#db1e1e']"
              id="car-chart"
              xtitle="Time"
              ytitle="Number of Cars"
              empty="No data"
              :dataset="{ borderWidth: 2 }"
            ></area-chart>
          </v-col>
          </v-card>

          <v-card
            class="d-flex ml-3 mb-4 pt-1 px-5 flex-wrap"
            width="750"
            height="380"
            outlined
          >
          <v-col>
            <h1 class="d-flex justify-center mb-3 font-weight-regular">Truck Flow</h1>
            <area-chart
              :data="dataCountTruck"
              :colors="['#32a852']"
              id="truck-chart"
              xtitle="Time"
              ytitle="Number of Trucks"
              empty="No data"
              :dataset="{ borderWidth: 2 }"
            ></area-chart>
          </v-col>
          </v-card>

          <v-card
            class="d-flex ml-3 pt-1 px-5 mb-4"
            width="750"
            height="380"
            outlined
          >
          <v-col>
             <h1 class="d-flex justify-center mb-3 font-weight-regular">Bike Flow</h1>
             <area-chart
              :data="dataCountBike"
              :colors="['#dbcb1e']"
              id="bike-chart"
              xtitle="Time"
              ytitle="Number of Bikes"
              empty="No data"
              :dataset="{ borderWidth: 2 }"
            ></area-chart>
          </v-col>
           
          </v-card>

          <v-card
            class="d-flex ml-3 pt-2 px-5"
            width="750"
            height="380"
            outlined
          >
          <v-col>
            <h1 class="d-flex justify-center mb-3 font-weight-regular">Double-Park Vehicles</h1>
            <area-chart
              :data="dataCountDoublePark"
              :colors="['#721edb']"
              id="doublePark-chart"
              xtitle="Time"
              ytitle="Number of Double-Parked Vehicles"
              empty="No data"
              :dataset="{ borderWidth: 2 }"
            ></area-chart>
          </v-col>
            
          </v-card>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>


<script>
import * as dayjs from "dayjs";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      valid: true,
      radioGroup: undefined,

      nameRules: [(v) => !!v],
      dateRules: [
        (v) => !!v || "Insert 2 dates",
        (v) =>
          /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])~\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/.test(
            v
          ) || "Insert 2 dates!",
      ],

      dataCountCar: [
        {
          name: "Car Count",
          data: {},
        },
      ],
      dataCountTruck: [
        {
          name: "Truck Flow",
          data: {},
        },
      ],
      dataCountBike: [
        {
          name: "Bike Flow",
          data: {},
        },
      ],
      dataCountDoublePark: [
        {
          name: "Double-Park Flow",
          data: {},
        },
      ],

      items: [
        {
          title: "Logout",
          icon: "mdi-logout",
          click() {
            this.$router.push("/");
          },
        },
        {
          title: "Processes",
          icon: "mdi-auto-fix",
          click() {
            console.log("processes");
            this.$router.push("processes");
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
      
      editedItem: {
        dates: [dayjs().format('YYYY-MM-DD'),dayjs().format('YYYY-MM-DD')],
        startHour: "00:00",
        endHour: "23:59",
        indicator: "",
      },

      defaultItem: {
        dates: [dayjs().format('YYYY-MM-DD'),dayjs().format('YYYY-MM-DD')],
        startHour: "00:00",
        endHour: "23:59",
        indicator: "",
      },
      sensors: [],

      menuStart: false,
      menuEnd: false,

      menu1: null,
      menu2: null,

      carCountChart: false,
      truckCountChart: false,
      bikeCountChart: false,
      doubleParkVehicles: false,
    };
  },

  methods: {
    async submitGetData() {
      if (this.carCountChart === true) await this.getData(1);
      if (this.truckCountChart === true) await this.getData(2);
      if (this.bikeCountChart === true) await this.getData(3);
      if (this.doubleParkVehicles === true) await this.getData(4);
    },
    async getSensors() {
      const urlDesktop = "127.0.0.1:5000";
      const urlRasp = "192.168.1.216:8080";

      const responseSensors = await fetch(`http://${urlDesktop}/sensors`);
      const sensors_res = await responseSensors.json();
      this.sensors = sensors_res;
    },

    async getData(indicator) {
      const urlDesktop = "127.0.0.1:5000";
      const urlRasp = "192.168.1.216:8080";

      const sensor = this.radioGroup;
      const dates = this.editedItem.dates;

      const startHour = this.editedItem.startHour;
      const endHour = this.editedItem.endHour;

      const startTime = dayjs(dates[0] + " " + startHour).toISOString();
      const endTime = dayjs(dates[1] + " " + endHour).toISOString();

      let id = parseInt(indicator);

      const data_json = await fetch(
        `http://${urlDesktop}/chart?sensor=${sensor}&startTime=${startTime}&endTime=${endTime}&indicator=${id}`
      );
      const data_array = await data_json.json();
      const data = Object.assign({}, ...data_array);
      let chart;
      if (id === 1) {
        this.dataCountCar[0].data = data;
        chart = Chartkick.charts["car-chart"];
        chart.updateData(this.dataCountCar);
      }
      if (id === 2) {
        this.dataCountTruck[0].data = data;
        chart = Chartkick.charts["truck-chart"];
        chart.updateData(this.dataCountTruck);
      }
      if (id === 3) {
        this.dataCountBike[0].data = data;
        chart = Chartkick.charts["bike-chart"];
        chart.updateData(this.dataCountBike);
      }
      if (id === 4) {
        this.dataCountDoublePark[0].data = data;
        chart = Chartkick.charts["doublePark-chart"];
        chart.updateData(this.dataCountDoublePark);
      }
    },

    handleClick(index) {
      this.items[index].click.call(this);
    },
  },
  computed: {
    ...mapGetters(["isLoggedIn"]),

    dateRangeText() {
      return this.editedItem.dates.join("~");
    },
  },
  async mounted() {
    await this.getSensors();

    await this.getData(1);
    await this.getData(2);
    await this.getData(3);
    await this.getData(4);

  },
};
</script>
