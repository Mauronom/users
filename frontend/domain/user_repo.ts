import { User } from "./user"
export abstract class UserRepo {
    abstract create(user: User): Promise<void> ;
    abstract find_all(): Promise<Array<User>>;
}
