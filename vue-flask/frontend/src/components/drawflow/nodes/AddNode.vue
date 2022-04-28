<template>
  <div class="card-devices" >
     <div class="header">
        <h1> Test </h1>
     </div>
    <div class="body" >
       <span @click="onClick">Name :</span>
     </div>
  </div>
</template>

<script>
export default {
  methods: {
    onClick() {
      alert("hello-drawflow");
    }
  }
}
</script>