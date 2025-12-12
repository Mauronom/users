import { User } from '../domain/user'
import { UserRepo } from '../domain/user_repo'
import { v4 as uuid_gen } from 'uuid';

export class CreateUser {
    user_repo: UserRepo;
    user: User;
    screen_data: any;
    constructor(user_repo: UserRepo, screen_data: any) {
        this.user_repo = user_repo;

        let uuid = uuid_gen();
        let username = screen_data["username"];
        let email = screen_data["email"];
        let dni = screen_data["dni"];
        this.user = new User(uuid, username, email, dni);

        this.screen_data = screen_data;
    }
    execute() {

        //check email validity
        if(!isValidEmail(this.user.email)){
            this.screen_data["result"] = "Email incorrecte";
            return;
        }

        let duplicate = this.user_repo.find_by_field("username", this.screen_data["username"]);
        if(duplicate){
            this.screen_data["result"]=`l'usuari ${this.screen_data["username"]} ja existeix`;
            return;
        }


        this.user_repo.save(this.user);
        this.screen_data["result"] = `L'usuari ${this.user.username} s'ha creat correctament`
    }
}


function isValidEmail(email: string) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
