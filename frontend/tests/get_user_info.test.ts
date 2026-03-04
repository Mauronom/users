
import {GetUserInfo} from "../app/get_user_info"
import {MemoryUserRepo} from "../infra/repos"
import {User} from "../domain/user"

describe ('Get User Info Tests', ()=>{
    it("test 1: GetUserInfo returns nothing if the username doesn't exist", async ()=>{
        let user_repo = new MemoryUserRepo([]);
        let screen_data = {shown_user: {selected_username:'u1', user_info: {username: "", email: "", dni: "" , error: ""}}};
        let q = new GetUserInfo(user_repo,screen_data);
        let exec = q.execute()
        expect(exec).toBeInstanceOf(Promise)
        await exec
        let user = await exec;
        expect(user).toBe(null);
        expect(screen_data.shown_user.user_info.username).toBe('');
        expect(screen_data.shown_user.user_info.error).toBe('User not found');
    });

    it("test 2: GetUserInfo returns the right user", async ()=>{
        let u = new User("1", "u1", "u1@test.com", "12345678A");
        let screen_data = {shown_user: {selected_username:'u1', user_info: {username: "", email: "", dni: "", error: ""}}};
        let user_repo = new MemoryUserRepo([u]);
        let q = new GetUserInfo(user_repo, screen_data);
        let exec = q.execute()
        expect(exec).toBeInstanceOf(Promise)
        await exec
        let user = await exec;
        console.log(user);
        expect(user.username).toBe("u1");
        expect(screen_data.shown_user.user_info.error).toBe('');
        expect(screen_data.shown_user.user_info.username).toBe('u1');
        expect(screen_data.shown_user.user_info.email).toBe('u1@test.com');
        expect(screen_data.shown_user.user_info.dni).toBe('12345678A');

    });
});
