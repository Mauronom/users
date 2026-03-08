import { User } from "../domain/user";
import { UserRepo } from "../domain/user_repo";


export class GetUserInfo {
    user_repo: UserRepo;
    username: string;
    screen_data;

    constructor(user_repo: UserRepo, screen_data: any) {
        this.user_repo = user_repo;
        this.screen_data = screen_data
        this.username = screen_data.shown_user.selected_username;
    }

    async execute(): Promise<User | null> {
        let user = await this.user_repo.find_by_username(this.username);
        if (!user) {
            this.screen_data.shown_user.user_info.username = ''
            this.screen_data.shown_user.user_info.email = ''
            this.screen_data.shown_user.user_info.dni = ''
            this.screen_data.shown_user.user_info.error = 'User not found'
            return null;
        }
        this.screen_data.shown_user.user_info.username = user.username
        this.screen_data.shown_user.user_info.email = user.email
        this.screen_data.shown_user.user_info.dni = user.dni
        this.screen_data.shown_user.user_info.error = ""
        return user;
    }

}
