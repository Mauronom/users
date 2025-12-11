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
    }
}
