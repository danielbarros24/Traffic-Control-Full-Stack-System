<template>
<v-text-field
  label="Regular"
  placeholder="Placeholder"
  solo
  dense
></v-text-field>
</template>

<script>
export default {
  props: ['readonly', 'emitter', 'ikey', 'getData', 'putData'],
  data() {
    return {
      value: Math.floor(Math.random() * 50),
    }
  },
  methods: {
    change(e){
      this.value = +e.target.value;
      this.update();
    },
    update() {
      if (this.ikey) {
        this.putData(this.ikey, this.value)
      }
      this.emitter.trigger('process');
    }
  },
  mounted() {
    this.value = this.getData(this.ikey);
  }
}
</script>