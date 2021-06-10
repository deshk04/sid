import { hostType } from '../environments/hosttype';
export let HOST_API: string;
export let HOST_ROOT: string;

// if (hostType === 'prod') {
//     // replace with your prod url
//     HOST_API = 'http://localhost:8080/api/';
//     HOST_ROOT = 'http://localhost:8080/';

// }
// else if (hostType === 'uat'){
//     // replace with your uat env
//     HOST_API = 'http://localhost:8080/api/';
//     HOST_ROOT = 'http://localhost:8080/';

// }
// else {
//     // replace with your dev env
//     HOST_API = 'http://localhost:8080/api/';
//     HOST_ROOT = 'http://localhost:8080/';
// }


HOST_API = 'http://localhost:8080/api/';
HOST_ROOT = 'http://localhost:8080/';
