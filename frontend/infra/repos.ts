import { User } from '../domain/user'
import { UserRepo } from '../domain/user_repo'

export class MemoryUserRepo implements UserRepo {
    users: Record<string, User>;

    constructor(users: Array<User>) {
        this.users = {};
        users.forEach(user => {
            this.users[user.uuid] = user;
        });
    }

    save(user: User): void {
        this.users[user.uuid] = user.clone();
    }

    find_all(): Array<User> {
        let res = new Array;
        let users_array = Object.values(this.users);
        for ( const user of users_array){
            res.push(user.clone());
        }
        return res;
        
    }
}
