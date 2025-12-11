import { User } from '../domain/user'
import { UserRepo} from '../domain/user_repo'
export class CreateUser {
    user_repo : UserRepo;
    user : User;
    constructor(user_repo : UserRepo, screen_data : any ){
        this.user_repo = user_repo;
        let username = screen_data["username"];
        let email = screen_data["email"];
        let dni = screen_data["dni"];
        this.user = new User(username, email, dni);
    }
}
