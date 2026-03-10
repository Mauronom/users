<template>

    <div class="my-component">
        <div class="page">
            <div class="form">
                <h2>{{ title }}</h2>

                <div class="user-info-input">
                    <label>Nom d'usuari:</label><input v-model="screen_data.username"></input>
                    <label>Correu electrònic:</label><input v-model="screen_data.email"></input>
                    <label>DNI:</label><input v-model="screen_data.dni"></input>
                    <p :class="screen_data.message_color ">{{ screen_data.result }}</p>
                    <button @click="createUser">Crea l'Usuari</button>

                </div>
                <button @click="showUsers">Mostra els usuaris creats</button>
                <div v-for="u in screen_data.users_list.split(',')" :key="u">  
                    <button @click="showUserInfo(u)">{{u}}</button>
                </div>
            </div>
        <div class="show-user-info">
                <h3>User Info</h3>
                <h4>Username:</h4>
                <p>{{ screen_data.shown_user.user_info.username }}</p>
                <h4>Email:</h4>
                <p>{{ screen_data.shown_user.user_info.email }}</p>
                <h4>DNI:</h4>
                <p>{{ screen_data.shown_user.user_info.dni }}</p>
                <p>{{screen_data.shown_user.user_}}</p>
        </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { CreateUser } from "../app/create_user"
import { GetUsers } from "../app/get_users"
import { GetUserInfo } from "../app/get_user_info"
import { APIUserRepo } from "./repos";
import { MemoryUserRepo } from "./repos";
import { v4 as uuid_gen } from 'uuid';


export default Vue.extend({
    name: 'CreateUser',

    // ----------------------------------
    // Dades reactives del component
    // ----------------------------------
    data() {
        const screen_data = { 
            username: "", 
            email: "", 
            dni: "", 
            result: "Crea Usuari", 
            message_color: 'black', 
            users_list: '', 
            shown_user: {selected_username:'', user_info: {username: "", email: "", dni: "" , error: ""}}};
        // const repo = new MemoryUserRepo([]);
        const repo = new APIUserRepo('http://0.0.0.0:8000');
        return {
            title: 'Crea un Usuari',
            counter: 0,
            screen_data,
            repo,
            cmd: new CreateUser(repo, screen_data, uuid_gen),
            query: new GetUsers(repo, screen_data),
            query_get_user_info: new GetUserInfo(repo,screen_data),
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
        showUserInfo(u : string) {
            this.screen_data.shown_user.selected_username = u.trim()
            this.query_get_user_info = new GetUserInfo(this.repo, this.screen_data)
            this.query_get_user_info.execute()
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

.page {
    display: flex;
    flex-direction: row;
    gap: 100px;
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
