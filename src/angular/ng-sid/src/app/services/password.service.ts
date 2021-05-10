import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PasswordService {
  private chgPasswdUrl = HOST_API + 'updatepassword/';  // URL to web API

  constructor(private http: HttpClient) { }

  changePasswd(formData: any): Observable<any> {

    return this.http.post<any>(
      this.chgPasswdUrl,
      formData.value
    );

  }


}
