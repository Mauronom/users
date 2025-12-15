<template>
    <div id="app">
      <h1>Usuaris</h1>
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
  