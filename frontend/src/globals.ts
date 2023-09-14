import { EUser, Key } from "./types";


let globals: {
    usertype: EUser,
    username: string,
    password: string,
    companyId: Key,
    developerId: Key
} = {
    usertype: EUser.NONE,
    username: '',
    password: '',
    companyId: '',
    developerId: 1,
}

export default globals