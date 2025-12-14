import {GetUsers} from "../app/get_users"
import {MemoryUserRepo} from "../infra/repos"
import {User} from "../domain/user"

describe ('Get User Tests', ()=>{
    it("test 1: GetUsers with empty user repo returns empty array", ()=>{
        let user_repo = new MemoryUserRepo([]);
        let q = new GetUsers(user_repo);
        let users = q.execute();
        expect(users.length).toBe(0);
    });

    it("test 2: GetUsers returns the right user", ()=>{
        let u = new User("1", "u1", "u1@test.com", "12345678A");
        let user_repo = new MemoryUserRepo([u]);
        let q = new GetUsers(user_repo);
        let users = q.execute();
        expect(users.length).toBe(1);
        expect(users[0].username).toBe("u1");
    });
});
