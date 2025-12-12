
export class User {
    uuid: string;
    username: string;
    email: string;
    dni: string;
    constructor(uuid: string, username: string, email: string, dni: string) {
        if(!isValidEmail(email)){
            throw new Error('InvalidEmail')
        }
        this.uuid = uuid;
        this.username = username;
        this.email = email;
        this.dni = dni;
    }
    clone() {
         return new User(this.uuid, this.username, this.email, this.dni);
    }
}

function isValidEmail(email: string) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

