export class User {
    uuid: string;
    username: string;
    email: string;
    dni: string;
    constructor(uuid: string, username: string, email: string, dni: string) {
        this.uuid = uuid;
        this.username = username;
        this.email = email;
        this.dni = dni;
    }
}
