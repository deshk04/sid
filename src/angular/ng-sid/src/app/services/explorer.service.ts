import { HOST_API } from '../app.config';
import { Observable } from 'rxjs';

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { IExplorerRecords } from '../models/explorer';

@Injectable({
  providedIn: 'root'
})
export class ExplorerService {
  private getTreebyIdUrl = HOST_API + 'gets3tree/';  // URL to web API
  private getS3file = HOST_API + 'gets3file/';  // URL to web API

  constructor(private http: HttpClient) { }

  getTreebyId(conn_id: number) {
    let params = new HttpParams().set('conn_id', String(conn_id));

    return this.http.get<IExplorerRecords>(
      this.getTreebyIdUrl,
      { params: params }
    );

  }

  downloadS3file(conn_id: number, filename: string): Observable<Blob> {
    let params = new HttpParams().set('conn_id', String(conn_id)).set(
      'filename', String(filename)
    );
    const options = {params, responseType: 'blob' as 'json'};

    return this.http.get<Blob>(
      this.getS3file,
      options
    );

  }

}
