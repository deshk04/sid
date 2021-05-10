export interface IUserProfile {
    first_name: string;
    last_name: string;
    email_id: string;
    role: number;
    photo: string;
    isLoggedIn: boolean;
}


// export interface IUserProfileRecord {
//     num_of_pages: number;
//     status: string;
//     message: string;
//     num_of_records: number;
//     records: Array<IUserProfile>;
// }

export interface IUserInput {
    username: string;
    password: string;
}

// export interface IUserAuthServ {
//     message: string;
// }

// export interface IUserAuthRecord {
//     num_of_pages: number;
//     status: string;
//     message: string;
//     num_of_records: number;
//     records: Array<IUserAuthServ>;
// }
