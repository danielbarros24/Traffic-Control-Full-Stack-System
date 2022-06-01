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

.node .control input, .node .input-control input {
  width: 140px;
}

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

