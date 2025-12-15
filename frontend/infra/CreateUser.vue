<template>
    <div class="my-component">
      <!-- Mostrem una dada del component -->
      <h2>{{ title }}</h2>
  
      <!-- Mostrem el valor reactiu -->
      <p>Counter: {{ counter }}</p>
  
      <!-- Botó que crida un mètode -->
      <button @click="incrementCounter">Incrementa</button>
      {{ screen_data }}
      <input v-model="screen_data.username" />
      <!-- Mostrem un valor computat -->
      <p>{{ counterMessage }}</p>
      {{ screen_data.result }}
    </div>
  </template>
  
  <script lang="ts">
  import Vue from 'vue'
  
  export default Vue.extend({
    name: 'CreateUser',
  
    // ----------------------------------
    // Dades reactives del component
    // ----------------------------------
    data() {
       return {
        title: 'Hola, Vue 2 amb TypeScript!',
        counter: 0, // valor inicial del comptador
        screen_data: {username:''},
        cmd:undefined
      }
    },
  
    // ----------------------------------
    // Computed properties: recalculades automàticament quan les dades canvien
    // ----------------------------------
    computed: {
      counterMessage(): string {
        return this.counter > 0
          ? `Has incrementat el comptador ${this.counter} vegades`
          : 'Encara no has clicat el botó'
      },
    },
  
    // ----------------------------------
    // Mètodes del component
    // ----------------------------------
    methods: {
      // Incrementa el comptador
      incrementCounter() {
        this.counter += 1
        this.title='hola'
      },
    },
  
    // ----------------------------------
    // Hooks del cicle de vida
    // ----------------------------------
  
    // Executat **immediatament després de crear el component**, abans de renderitzar
    created() {
      console.log('Component creat! Aquí podem inicialitzar dades o fer peticions')
    },
  
    // Executat **després que el component s’hagi muntat al DOM**
    mounted() {
      console.log('Component muntat al DOM! Aquí podem manipular elements del DOM o cridar APIs')
    },
  })
  </script>
  
  <style scoped>
  .my-component {
    font-family: Arial, sans-serif;
    padding: 20px;
    border: 1px solid #ccc;
    display: inline-block;
  }
  
  button {
    padding: 10px 20px;
    font-size: 16px;
  }
  </style>
  