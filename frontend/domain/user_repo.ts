import { User } from "./user"
export abstract class UserRepo {
    users_uuid_dict: any;

    abstract save(user: User): void;
    abstract find_all(): Array<User>;
    abstract find_by_field(field: string, value: string): User;
}
