import { User } from "./user"
export abstract class UserRepo {
    users_uuid_dict: any;

    abstract create(user: User): Promise<void> ;
    abstract find_all(): Promise<Array<User>>;
    abstract find_by_field(field: string, value: string): Promise<User> ;
}
