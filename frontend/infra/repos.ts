import { User } from '../domain/user'
import { UserRepo } from '../domain/user_repo'

export class MemoryUserRepo implements UserRepo {
    users_uuid_dict: Record<string, User>;
    users_username_dict: Record<string, User>;
    users_email_dict: Record<string, User>;
    users_dni_dict: Record<string, User>;

    constructor(users: Array<User>) {
        this.users_uuid_dict = {};
        this.users_username_dict = {};
        this.users_email_dict = {};
        this.users_dni_dict = {};
        users.forEach(passed_user => {
            let user = passed_user.clone();
            this.users_uuid_dict[user.uuid] = user;
            this.users_username_dict[user.username] = user;
            this.users_email_dict[user.email] = user;
            this.users_dni_dict[user.dni] = user;
        });
    }

    create(passed_user: User): void {
        let user = passed_user.clone();
        if (user.uuid in this.users_uuid_dict) {
            throw new Error("UuidClash");
        }
        if (user.username in this.users_username_dict) {
            throw new Error("UsernameExists");

        }
        if (user.email in this.users_email_dict) {
            throw new Error("EmailExists");

        }
        if (user.dni in this.users_dni_dict) {
            throw new Error('DniExists')
        }
        this.users_uuid_dict[user.uuid] = user;
        this.users_username_dict[user.username] = user;
        this.users_email_dict[user.email] = user;
        this.users_dni_dict[user.dni] = user;
    }

    find_all(): Array<User> {
        let res = new Array;
        let users_array = Object.values(this.users_uuid_dict);
        for (const user of users_array) {
            res.push(user.clone());
        }
        return res;

    }

    find_by_field(field: string, value: string): User {
        switch (field) {
            case "uuid":
                return this.users_uuid_dict[value];
            case "username":
                return this.users_username_dict[value];
            case "email":
                return this.users_email_dict[value];
            case "dni":
                return this.users_dni_dict[value];
            default:
                throw new Error("field not valid");
        }


    }
}
