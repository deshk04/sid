import { Injectable, NgZone } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, BehaviorSubject, pipe, EMPTY } from 'rxjs';
import { finalize } from "rxjs/operators";

import { catchError, switchMap, filter, take } from 'rxjs/operators';
import { Router } from '@angular/router';

import { Tokens, DecodedToken } from '../models/tokens';

import { UserAuthService } from '../services/auth.service';
import { HOST_API } from '../app.config';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  constructor(private userAuthService: UserAuthService,
    private zone: NgZone,
    private router: Router) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let token = this.userAuthService.token;
    if (token) {
      request = this.addToken(request, token);
    }

    return next.handle(request).pipe(catchError(error => {
      if (request.url.endsWith("/sid-token/")) {
        return throwError(error);
      }
      if (error instanceof HttpErrorResponse && error.status === 401) {
        // if 401 due to expired refresh token, need to relogin
        if (request.url.endsWith("/token/refresh/")) {
          this.userAuthService.logout();
          this.zone.run(() => this.router.navigate(['/login']));
          return EMPTY;
        }
        return this.handle401Error(request, next);
      }
      else {
        return throwError(error);
      }
    })
    ) as Observable<HttpEvent<any>>;
  }

  private addToken(request: HttpRequest<any>, token: string) {
    return request.clone({
      setHeaders: {
        'Authorization': `Bearer ${token}`
      }
    });
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler) {
    // console.log('handle 401');
    if (!this.isRefreshing) {
      // console.log('Refreshing...');
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null)

      return this.userAuthService.refreshToken().pipe(
        switchMap((token) => {
          // console.log('inside switchmap....')
          this.isRefreshing = false;
          return next.handle(this.addToken(request, token));
        })).pipe(finalize(() => {
          // console.log('inside finalize');
          this.isRefreshing = false;
      }));

      // return this.userAuthService.refreshToken().subscribe(
      //   (token) => {
      //     this.isRefreshing = false;
      //     this.addToken(request, token)
      //   }
      // )

    } else {
      // console.log('not refreshing...so sending it to client')

          // return next.handle(this.addToken(request,
          //   this.userAuthService.token));

          return this.refreshTokenSubject.pipe(
            filter(token => token != null),
            take(1),
            switchMap(access => {
              return next.handle(this.addToken(request, access));
            }));


      }
  }
}