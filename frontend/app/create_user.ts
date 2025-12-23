import { User } from '../domain/user'
import { UserRepo } from '../domain/user_repo'

export class CreateUser {
    user_repo: UserRepo;
    screen_data: any;
    uuid_gen: any;
    error: boolean;
    constructor(user_repo: UserRepo, screen_data: any, uuid_gen: any) {
        this.user_repo = user_repo;
        this.screen_data = screen_data;
        this.uuid_gen = uuid_gen
        this.error = false;
    }
    execute() {

        let uuid = this.uuid_gen();
        let username = this.screen_data["username"];
        let email = this.screen_data["email"];
        let dni = this.screen_data["dni"];
        let user
        try {
            user = new User(uuid, username, email, dni);
        } catch (e: any) {
            if (e.message == 'InvalidEmail') {
                this.screen_data["result"] = "Email incorrecte";
            } else {
                this.screen_data["result"] = "Error creant usuari";
            }
            this.error = true;
            this.screen_data['message_color'] = 'error-color'
            return
        }

        try {
            this.user_repo.create(user);
        } catch (e: any) {
            if (e.message == 'UsernameExists') {
                this.screen_data["result"] = `l'usuari ${this.screen_data["username"]} ja existeix`;
            }
            else if (e.message == 'EmailExists') {
                this.screen_data["result"] = `l'email ${this.screen_data["email"]} ja existeix`;
            }
            else if (e.message == 'DniExists') {
                this.screen_data["result"] = `El DNI ${this.screen_data["dni"]} ja existeix`;
            } else {
                this.screen_data["result"] = "Error creant usuari";
            }
            this.screen_data['message_color'] = 'error-color'
            this.error = true;
            return;

        }
        this.screen_data['message_color'] = 'default-color'
        this.error = false;
        this.screen_data["result"] = `L'usuari ${user.username} s'ha creat correctament`
    }
}


