import { User } from "../domain/user";
import { UserRepo } from "../domain/user_repo";


export class GetUsers {
    user_repo : UserRepo;

    constructor(user_repo : UserRepo){
        this.user_repo = user_repo;
    }

    execute(){
        return this.user_repo.find_all();
    }

}
