import { User } from './domain/user'
import { CreateUser} from './app/create_user'
import {MemoryUserRepo} from './infra/repos'

let user = new User("jaume", "sgsdf", "1234543A");

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
console.log(cmd.user.username);
console.log(cmd.user.email);
console.log(cmd.user.dni);
console.log("");
