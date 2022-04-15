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

    <v-col>
      <v-btn
        color="secondary"
        depressed
        elevation="4"
        large
        raised
        rounded
        mx-auto
      > <v-icon class="mr-3">mdi-plus</v-icon>Create automation
      </v-btn>
    </v-col>
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
  }),

  methods: {
    handleClick(index) {
      this.items[index].click.call(this);
    },
    clickLogo() {
      this.$router.push("dashboard");
    },
  },
};
</script>