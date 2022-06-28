<template>
<v-text-field class="d-flex justify-start mr-8"
  placeholder="Add duration in seconds"
  solo
  dense
  v-model="reteValue"
></v-text-field>
</template>


<script>
export default {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData'],
  data() {
    return {
      value: 0
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

 