<template>
  <v-row class="mt-2 mb-1 ml-1">
    <v-menu>
      <template v-slot:activator="{ attrs, on }">
        <v-btn
          color="primary"
          class="white--text font-weight-bold"
          v-bind="attrs"
          v-on="on"
        >
          Zone
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="item in items"
          :key="item"
          link
        >
          <v-list-item-title v-text="item"></v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-row>
</template>


<script>
export default {
  props: ["readonly", "emitter", "ikey", "getData", "putData"],
  data:() => {

    items: [
        { title: 'Click Me' },
        { title: 'Click Me' },
        { title: 'Click Me' },
        { title: 'Click Me 2' },
      ];
    return {
      value: 0
    };
    
  },
  methods: {
    change(e) {
      this.value = e.target.value;
      this.update();
    },
    update() {
      if (this.ikey) this.putData(this.ikey, this.value);
      this.emitter.trigger("process");
    }
  },
  mounted() {
    this.value = this.getData(this.ikey);
  }
}
</script>

<style scoped>
select, input {
  width: 100%;
  border-radius: 30px;
  background-color: white;
  padding: 2px 6px;
  border: 1px solid #999;
  font-size: 110%;
  width: 170px;
}
</style>
