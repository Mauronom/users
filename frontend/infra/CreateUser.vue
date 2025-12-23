<template>
    <div class="my-component">
        <h2>{{ title }}</h2>

        <div class="user-info-input">
            <label>Nom d'usuari:</label><input v-model="screen_data.username"></input>
            <label>Correu electrònic:</label><input v-model="screen_data.email"></input>
            <label>DNI:</label><input v-model="screen_data.dni"></input>
            <p :class="screen_data.message_color ">{{ screen_data.result }}</p>
            <button @click="createUser">Crea l'Usuari</button>

        </div>
        <button @click="showUsers">Mostra els usuaris creats</button>
        <p>{{ screen_data.users_list }}</p>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { CreateUser } from "../app/create_user"
import { GetUsers } from "../app/get_users"
import { MemoryUserRepo } from "./repos"
import { v4 as uuid_gen } from 'uuid';


export default Vue.extend({
    name: 'CreateUser',

    // ----------------------------------
    // Dades reactives del component
    // ----------------------------------
    data() {
        const screen_data = { username: "", email: "", dni: "", result: "Crea Usuari", message_color: 'black', users_list: '' };
        const repo = new MemoryUserRepo([]);
        return {
            title: 'Crea un Usuari',
            counter: 0,
            screen_data,
            cmd: new CreateUser(repo, screen_data, uuid_gen),
            query: new GetUsers(repo, screen_data),
            usersList: "",
        }
    },

    // ----------------------------------
    // Computed properties: recalculades automàticament quan les dades canvien
    // ----------------------------------
    computed: {

    },

    // ----------------------------------
    // Mètodes del component
    // ----------------------------------
    methods: {
        // Incrementa el comptador
        showUsers() {
            this.query.execute()
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

.default-color {
    color: black;
}

.error-color {
    color: red;
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
