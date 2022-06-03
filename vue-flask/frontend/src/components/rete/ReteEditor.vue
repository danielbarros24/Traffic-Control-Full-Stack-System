<template>
  <div id="rete" ref="rete"></div>
</template>

<script>
import init from "@/node-editor";

export default {
  props: ['value'],
  async mounted() {
    const { editor } = await init(this.$refs.rete)
    this.$emit('input', editor)
  }
};
</script>

<style scoped>
#rete {
  z-index: 999;
  background:
    conic-gradient(from 90deg at 1px 1px,#0000 90deg,#dddddd 0) 
    0 0/50px 50px;
}

</style>

