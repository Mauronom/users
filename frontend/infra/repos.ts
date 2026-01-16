import { User } from '../domain/user'
import { UserRepo } from '../domain/user_repo'

export class MemoryUserRepo implements UserRepo {
    users_uuid_dict: Record<string, User>;
    users_username_dict: Record<string, User>;
    users_email_dict: Record<string, User>;
    users_dni_dict: Record<string, User>;

    constructor(users: Array<User>) {
        this.users_uuid_dict = {};
        this.users_username_dict = {};
        this.users_email_dict = {};
        this.users_dni_dict = {};
        users.forEach(passed_user => {
            let user = passed_user.clone();
            this.users_uuid_dict[user.uuid] = user;
            this.users_username_dict[user.username] = user;
            this.users_email_dict[user.email] = user;
            this.users_dni_dict[user.dni] = user;
        });
    }

    async create(passed_user: User): Promise<void> {
        let user = passed_user.clone();
        if (user.uuid in this.users_uuid_dict) {
            throw new Error("UuidClash");
        }
        if (user.username in this.users_username_dict) {
            throw new Error("UsernameExists");

        }
        if (user.email in this.users_email_dict) {
            throw new Error("EmailExists");

        }
        if (user.dni in this.users_dni_dict) {
            throw new Error('DniExists')
        }
        this.users_uuid_dict[user.uuid] = user;
        this.users_username_dict[user.username] = user;
        this.users_email_dict[user.email] = user;
        this.users_dni_dict[user.dni] = user;
    }

    async find_all(): Promise<Array<User>> {
        let res = new Array;
        let users_array = Object.values(this.users_uuid_dict);
        for (const user of users_array) {
            res.push(user.clone());
        }
        return res;

    }

}


export class APIUserRepo implements UserRepo {

    constructor(
        private readonly baseUrl: string
    ) {}

    /* =======================
       COMMANDS
    ======================== */

    async create(passed_user: User): Promise<void> {
        const response = await fetch(
            `${this.baseUrl}/command/create.user`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    uuid: passed_user.uuid,
                    username: passed_user.username,
                    email: passed_user.email,
                    dni: passed_user.dni
                })
            }
        )

        if (!response.ok) {
            const errorText = await response.text()
            throw new Error(errorText)
        }
    }

    async find_all(): Promise<Array<User>> {
        const response = await fetch(
            `${this.baseUrl}/query/get.users`
        )

        if (!response.ok) {
            throw new Error('QueryError')
        }

        const data: string[] = await response.json()

        return data.map(this.parseUserString)
    }

    
    private parseUserString(userStr: string): User {
        // Ex: "User(uuid=1, username=u1, email=u1@test.com, dni=12345678A)"
        const regex =
            /uuid=(.*?), username=(.*?), email=(.*?), dni=(.*?)\)/
        const match = userStr.match(regex)

        if (!match) {
            throw new Error('InvalidUserFormat')
        }

        const [, uuid, username, email, dni] = match
        return new User(uuid, username, email, dni)
    }

}
