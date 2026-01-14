import { MemoryUserRepo } from '../infra/repos'
import { CreateUser } from '../app/create_user'
import { User } from '../domain/user'
import { v4 as uuid_gen } from 'uuid';


describe('Create User Tests', () => {

    it('test 1',async () => {
        let screen_data = {username:'user1',email:'user@test.com',dni:'12345678A', result:'', message_color:'default-color'}
        let user_repo = new MemoryUserRepo([])
        let cmd = new CreateUser(user_repo, screen_data, uuid_gen)
        let exec = cmd.execute()
        expect(exec).toBeInstanceOf(Promise)
        await exec
        expect(screen_data.result).toBe("L'usuari user1 s'ha creat correctament")
        expect(screen_data.message_color).toBe("default-color")
        expect((await user_repo.find_all()).length).toBe(1)
        expect((await user_repo.find_all())[0].username).toBe('user1')
        screen_data.username='user2'
        screen_data.email='user2@test.com',
        screen_data.dni='22345678A'
        await cmd.execute()
        expect((await user_repo.find_all()).length).toBe(2)

    })
    it('test 2', async () => {
        let screen_data = {username:'user1',email:'usertest.com',dni:'12345678A', result:'', message_color:'default-color'}
        let user_repo = new MemoryUserRepo([])
        let cmd = new CreateUser(user_repo, screen_data, uuid_gen)
        let exec = cmd.execute()
        expect(exec).toBeInstanceOf(Promise)
        await exec
        expect(screen_data.result).toBe("Email incorrecte")
        expect(screen_data.message_color).toBe("error-color")
        expect((await user_repo.find_all()).length).toBe(0)
    })
    it('test 3', async () => {
        let screen_data = {username:'user1',email:'user@test.com',dni:'12345678A', result:'', message_color:'default-color'}
        let user_repo = new MemoryUserRepo([new User('uuid','user1','user@test.com','12345678A')])
        let cmd = new CreateUser(user_repo, screen_data, uuid_gen)
        let exec = cmd.execute()
        expect(exec).toBeInstanceOf(Promise)
        await exec
        expect(screen_data.result).toBe("l'usuari user1 ja existeix")
        expect(screen_data.message_color).toBe("error-color")
        expect((await user_repo.find_all()).length).toBe(1)
    })
})
