import { MemoryUserRepo } from '../infra/repos'
import { CreateUser } from '../app/create_user'
import { User } from '../domain/user'

describe('Create User Tests', () => {
    it('test 1',() => {
        let screen_data = {username:'user1',email:'user@test.com',dni:'12345678A', result:''}
        let user_repo = new MemoryUserRepo([])
        let cmd = new CreateUser(user_repo, screen_data)
        cmd.execute()
        expect(screen_data.result).toBe("L'usuari user1 s'ha creat correctament")
        expect(user_repo.find_all().length).toBe(1)
        expect(user_repo.find_all()[0].username).toBe('user1')
    })
    it('test 2',() => {
        let screen_data = {username:'user1',email:'usertest.com',dni:'12345678A', result:''}
        let user_repo = new MemoryUserRepo([])
        let cmd = new CreateUser(user_repo, screen_data)
        cmd.execute()
        expect(screen_data.result).toBe("Email incorrecte")
        expect(user_repo.find_all().length).toBe(0)
    })
    it('test 2',() => {
        let screen_data = {username:'user1',email:'user@test.com',dni:'12345678A', result:''}
        let user_repo = new MemoryUserRepo([new User('user1','user@test.com','12345678A')])
        let cmd = new CreateUser(user_repo, screen_data)
        cmd.execute()
        expect(screen_data.result).toBe("l'usuari user1 ja existeix")
        expect(user_repo.find_all().length).toBe(1)
    })
})
