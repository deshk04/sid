import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IConnectionRecords } from '../models/connection';
import { IDimRecords } from '../models/dimensions';

import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConnectionsService {
  private connUrl = HOST_API + 'getconnectors/';  // URL to web API
  private dimconnUrl = HOST_API + 'getdimconnectors/';  // URL to web API
  private updateconnUrl = HOST_API + 'updateconnector/';  // URL to web API

  constructor(private http: HttpClient) { }

  getConnections() {
    //    let params = new HttpParams().set('query', queryString);

    return this.http.get<IConnectionRecords>(
      this.connUrl,
      //        { params: params }
    );

  }
  getdimConnections() {
    //    let params = new HttpParams().set('query', queryString);

    return this.http.get<IDimRecords>(
      this.dimconnUrl,
      //        { params: params }
    );

  }

  updateConnection(data: any): Observable<any> {
    return this.http.post<any>(
      this.updateconnUrl,
      data.value
    );

  }

}
