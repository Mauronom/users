import { User } from "../domain/user";
import { UserRepo } from "../domain/user_repo";


export class GetUsers {
    user_repo : UserRepo;
    screen_data;

    constructor(user_repo : UserRepo, screen_data:any){
        this.user_repo = user_repo;
        this.screen_data = screen_data
    }

    execute(){
        this.screen_data.users_list = ''
        let users = this.user_repo.find_all();
        for(let i=0;i<users.length;i++){
        if(this.screen_data.users_list != ""){
            this.screen_data.users_list += ", ";
        }
        this.screen_data.users_list += users[i].username;
      }
      return this.user_repo.find_all();
    }

}
