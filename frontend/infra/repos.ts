import { User } from '../domain/user'

export class MemoryUserRepo {
    users: Array<User>;
    constructor(users: Array<User>) {
        this.users = users;
    }
}
