<template>
    <div id="app">
      <h1>Hola, Vue 2 amb TypeScript!</h1>
      <CreateUser />
    </div>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  import CreateUser from './CreateUser.vue'
  
  export default Vue.extend({
    name: 'App',
    components: {
      CreateUser,
    },
  })
  </script>
  
  <style>
  #app {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 50px;
  }
  </style>
  