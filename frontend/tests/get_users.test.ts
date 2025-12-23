import {GetUsers} from "../app/get_users"
import {MemoryUserRepo} from "../infra/repos"
import {User} from "../domain/user"

describe ('Get User Tests', ()=>{
    it("test 1: GetUsers with empty user repo returns empty array", ()=>{
        let user_repo = new MemoryUserRepo([]);
        let screen_data = {users_list:''}
        let q = new GetUsers(user_repo,screen_data);
        let users = q.execute();
        expect(users.length).toBe(0);
        expect(screen_data.users_list).toBe('');
    });

    it("test 2: GetUsers returns the right user", ()=>{
        let u = new User("1", "u1", "u1@test.com", "12345678A");
        let screen_data = {users_list:''}
        let user_repo = new MemoryUserRepo([u]);
        let q = new GetUsers(user_repo, screen_data);
        let users = q.execute();
        expect(users.length).toBe(1);
        expect(users[0].username).toBe("u1");
        expect(screen_data.users_list).toBe('u1');

    });
    it("test 3: GetUsers returns the right user", ()=>{
        let u = new User("1", "u1", "u1@test.com", "12345678A");
        let u2 = new User("2", "u2", "u2@test.com", "22345678A");
        let screen_data = {users_list:''}
        let user_repo = new MemoryUserRepo([u,u2]);
        let q = new GetUsers(user_repo, screen_data);
        let users = q.execute();
        expect(users.length).toBe(2);
        expect(users[0].username).toBe("u1");
        expect(screen_data.users_list).toBe('u1, u2');
        users = q.execute();
        expect(users.length).toBe(2);
        expect(users[0].username).toBe("u1");
        expect(screen_data.users_list).toBe('u1, u2');


    });
});
