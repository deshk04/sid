import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IDimRecords } from '../models/dimensions';

import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DimensionsService {
  private dimconnUrl = HOST_API + 'getdimensions/';  // URL to web API

  constructor(private http: HttpClient) { }

  getdimConnections() {
    //    let params = new HttpParams().set('query', queryString);

    return this.http.get<IDimRecords>(
      this.dimconnUrl,
      //        { params: params }
    );

  }

}
