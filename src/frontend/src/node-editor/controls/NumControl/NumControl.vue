<template>
  <v-text-field class="d-flex justify-start mr-6"
    :placeholder="placeholder"
    solo
    dense
    v-model="reteValue"
  ></v-text-field>
</template>
 
<script>
export default {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData', 'placeholder'],
  data() {
    return {
      value: 0,
    }
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
  }
}
</script>