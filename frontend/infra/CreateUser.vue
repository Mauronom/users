<template>
  <div class="my-component">
    <h2>{{ title }}</h2>

    <div class="user-info-input">
      <label>Nom d'usuari:</label><input v-model="screen_data.username"></input>
      <label>Correu electrònic:</label><input v-model="screen_data.email"></input>
      <label>DNI:</label><input v-model="screen_data.dni"></input>
      <p :style="{color: messageColor}">{{ createUserMessage}}</p>
      <button @click="createUser">Crea l'Usuari</button>

    </div>
    <button @click="showUsers">Mostra els usuaris creats</button>
    <p>{{ usersList }}</p>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { CreateUser } from "../app/create_user"
import { MemoryUserRepo } from "./repos"
import { v4 as uuid_gen } from 'uuid';


export default Vue.extend({
  name: 'CreateUser',

  // ----------------------------------
  // Dades reactives del component
  // ----------------------------------
  data() {
    const screen_data = { username: "", email: "", dni: "" ,result: "Crea Usuari"};
    const repo = new MemoryUserRepo([]);
    return {
      title: 'Crea un Usuari',
      counter: 0,
      screen_data,
      cmd: new CreateUser(repo, screen_data, uuid_gen),
      usersList: "",
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
    createUserMessage(): string {
      return this.screen_data.result;
    },
    messageColor(){
      if(this.cmd.error){
        return "red";
      }else{
        return "black";
      }
    }
  },

  // ----------------------------------
  // Mètodes del component
  // ----------------------------------
  methods: {
    // Incrementa el comptador
    showUsers() {
      let msg ="";
      let users = this.cmd.user_repo.find_all();
      for(let i=0;i<users.length;i++){
        if(msg != ""){
          msg += ", ";
        }
        msg += users[i].username;
      }
      this.usersList = msg;

    },
    createUser() {
      this.cmd.execute();
    },

  },

  // ----------------------------------
  // Hooks del cicle de vida
  // ----------------------------------

  // Executat **immediatament després de crear el component**, abans de renderitzar
  created() {
  },

  // Executat **després que el component s’hagi muntat al DOM**
  mounted() {
    console.log('Component muntat al DOM! Aquí podem manipular elements del DOM o cridar APIs')
  },
})
</script>

<style scoped>
.my-component {
  width: 20vw;
padding: 20px;
  border: 1px solid #ccc;
  display: inline-block;
}

.user-info-input {
  width: 20vw;
  display: flex;
  flex-direction: column;
  font-family: Arial, sans-serif;
}

button {
  padding: 10px 20px;
  font-size: 16px;
}
</style>
