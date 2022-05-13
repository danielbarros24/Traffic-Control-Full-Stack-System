<template>
  <v-select 
    :items="items" 
    v-model="reteValue"
    solo
  >
  </v-select>
</template>


<script>
export default {
  name: 'SelectControl',

  props: ['emitter', 'ikey', "getData", "putData", "items"],

  data() {
    return {
      value: ''
    };
  },

  computed: {
    reteValue: {
      get() {
        return this.value;
      },

      set(newValue) {
        this.value = newValue;

        this.putData(this.ikey, newValue);
        this.emitter.trigger('process');
      }
    }
  },

  mounted() {
    this.value = this.getData(this.ikey);
  },
};
</script>
