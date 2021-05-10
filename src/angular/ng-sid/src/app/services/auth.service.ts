import { Injectable, NgZone } from '@angular/core';
import { HttpClient, HttpInterceptor, HttpHeaders } from '@angular/common/http';
import { CanActivate, Router } from '@angular/router';
import { map, tap, shareReplay } from 'rxjs/operators';

import * as jwt_decode from 'jwt-decode';

import * as moment from "moment";

import { Observable, BehaviorSubject, throwError } from 'rxjs';

import { IUserInput, IUserProfile } from '../models/userprofile';
import { UserProfileDataService } from '../services/userprofiledata.service';

import { HOST_API } from '../app.config';
import { MatRadioChange } from '@angular/material/radio';


// import 'rxjs/add/observable/of';
// import 'rxjs/add/operator/do';

/*******************************************************************************
  Authorisation service
*******************************************************************************/


@Injectable()
export class UserAuthService {

    private loginurl = HOST_API + 'sid-token/';  // URL to web API
    private refreshurl = HOST_API + 'token/refresh/';  // URL to web API
    private logoffurl = HOST_API + 'logout/';  // URL to web API
    private headers = new HttpHeaders().set('Content-Type', 'application/json; charset=utf-8');

    private userProfile: IUserProfile = { first_name: '', last_name: '', email_id: '', role: null, photo: '', isLoggedIn: false };

    constructor(private http: HttpClient,
        private router: Router,
        private zone: NgZone,
        private userProfileDataService: UserProfileDataService) {

    }


    login(data: IUserInput): Observable<any> {
        return this.http.post<any>(
            this.loginurl,
            data,
            { headers: this.headers })
            .pipe(map(response => {
                this.setSession(response, false)
                return response;
            }))


    }

    setSession(authResult, refreshFlag) {
        const token = authResult.access;
        const payload = jwt_decode(token);
        const expiresAt = moment.unix(payload.exp);
        localStorage.setItem('token', token);
        this.setProfile();

        if (!refreshFlag) {
            localStorage.setItem('refresh', authResult.refresh);
        }
        localStorage.setItem('expires_at', JSON.stringify(expiresAt.valueOf()));

    }

    private setProfile() {
        const payload = jwt_decode(this.token);

        this.userProfile.first_name = payload.first_name;
        this.userProfile.last_name = payload.last_name;
        this.userProfile.email_id = payload.email;
        this.userProfile.photo = payload.photo;
        this.userProfile.isLoggedIn = true;
        this.userProfileDataService.profileRecord.next(this.userProfile);
    }

    get profile() {
        this.setProfile()
        return this.userProfile;
    }

    get token(): string {
        return localStorage.getItem('token');
    }
    get rToken(): string {
        return localStorage.getItem('refresh');
    }


    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        localStorage.removeItem('expires_at');
        this.userProfile.first_name = '';
        this.userProfile.last_name = '';
        this.userProfile.email_id = '';
        this.userProfile.isLoggedIn = false;
        this.userProfileDataService.profileRecord.next(this.userProfile);

    }

    refreshToken(): Observable<any> {
            return this.http.post<any>(
                this.refreshurl,
                { 'refresh': this.rToken },
                { headers: this.headers }
            ).pipe(
                map(response => {
                    console.log('setting new session');
                    this.setSession(response, true);
                    return this.token;
                })
            );
    }

    getExpiration() {
        const expiration = localStorage.getItem('expires_at');
        const expiresAt = JSON.parse(expiration);

        return moment(expiresAt);
    }

    isAccessExpired() {
        return moment().isBefore(this.getExpiration());

    }
    isLoggedIn() {
        //return moment().isBefore(this.getExpiration());
        if(this.token){
            return true;
        }
        return false;
    }

    isLoggedOut() {
        return !this.isLoggedIn();
    }
}

@Injectable()
export class AuthGuard implements CanActivate {

    constructor(private authService: UserAuthService, private router: Router) { }

    canActivate() {
        if (this.authService.token) {
            if (this.authService.isLoggedIn()) {
                //            return this.authService.refreshToken();
                return this.authService.isLoggedIn();
            } else {
                //    this.authService.logout();
                //    this.router.navigate(['login']);
                if (this.authService.token) {
                    this.authService.refreshToken().subscribe(
                        result => {
                            if (this.authService.isLoggedOut()) {
                                this.router.navigate['login'];
                                return false;
                            }
                        }
                    );
                    return true;
                }
                //return true;
            }
        }
    }
}