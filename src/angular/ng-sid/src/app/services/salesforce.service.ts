import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IJobsRecords, IJobModelRecords } from '../models/jobs';
import { ISFVerifyQueryRecords } from '../models/salesforce';

import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SalesforceService {
  private validateSFQueryUrl = HOST_API + 'validatesfquery/';

  constructor(private http: HttpClient) { }

  /* Post method */
  validateSFQuery(data: any): Observable<ISFVerifyQueryRecords> {
    const formData: FormData = new FormData();
    var postData = JSON.stringify(data);
    formData.append('data', postData);

    return this.http.post<ISFVerifyQueryRecords>(
        this.validateSFQueryUrl,
        formData
    );
  }



}
