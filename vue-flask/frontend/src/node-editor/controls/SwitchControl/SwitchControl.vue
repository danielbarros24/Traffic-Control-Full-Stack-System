<template>
  <v-switch
      v-model="reteValue"
      :label="`Invert: ${reteValue.toString()}`"
      hide-details
      color="white"
      dark
      class="font-weight-medium"
    ></v-switch>
</template>


<script>
export default {
  name: 'SwitchControl',

  props: ['emitter', 'ikey', "getData", "putData", "items"],

  data() {
    return {
      value: '',
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

<style scoped>

.v-select {
  width: 200px;
}
</style>