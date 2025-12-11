import {User} from "./user"
export abstract class UserRepo {
    users : any;

    abstract save(user : User) : void;
}
