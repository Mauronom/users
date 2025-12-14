<template>
    <button @click="inc">{{ value }}</button>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  
  export default Vue.extend({
    data() {
      return { value: 0 }
    },
    methods: {
      inc() {
        this.value++
      },
    },
  })
  </script>
  