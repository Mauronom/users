import { User } from './domain/user'
import { CreateUser} from './app/create_user'
import {MemoryUserRepo} from './infra/repos'

let user = new User("uuid","jaume", "sgsdf", "1234543A");

console.log("provant User class:");
console.log("--------------------------------------------");
console.log(user.username);
console.log(user.email);
console.log("");


console.log("provant CreateUser class:");
console.log("--------------------------------------------");
let screen_data = { username: 'user1', email: 'user@test.com', dni: '12345678A', result: '' }
let user_repo = new MemoryUserRepo([])
let cmd = new CreateUser(user_repo, screen_data)
console.log(cmd.user.uuid);
console.log(cmd.user.username);
console.log(cmd.user.email);
console.log(cmd.user.dni);
console.log("");


console.log("provant MemoryUserRepo class:");
console.log("--------------------------------------------");
cmd.execute();
let users = user_repo.find_all();
console.log(users[0]);


console.log("provant email check:");
console.log("--------------------------------------------");
screen_data = { username: 'user1', email: 'usertestcom', dni: '12345678A', result: '' }
cmd = new CreateUser(user_repo, screen_data)
cmd.execute();
users = user_repo.find_all();
console.log(users.length);
console.log(screen_data.result);

console.log("provant regex");
console.log("--------------------------------------------");
let jaume = "jaume";
let ok = /jaume/.test(jaume);
console.log(ok);
