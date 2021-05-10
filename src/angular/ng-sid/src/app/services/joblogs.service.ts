import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IJoblogsRecords } from '../models/joblogs';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JoblogsService {
  private joblogsUrl = HOST_API + 'getjoblogs/';  // URL to web API
  private downloadlogUrl = HOST_API + 'downloadlog/';  // URL to web API
  private jobrunByJobRunIdUrl = HOST_API + 'runjobbyjobrunid/';
  private joblogByIdUrl = HOST_API + 'getjoblogbyid/';  // URL to web API

  constructor(private http: HttpClient) { }

  getLogs(startDateString: string, endDateString: string) {
    const params = new HttpParams().set(
      'startdate', startDateString).set('enddate', endDateString);

    return this.http.get<IJoblogsRecords>(
      this.joblogsUrl,
      { params: params }
    );

  }
  getLogById(jobrun_id: string) {
    let params = new HttpParams().set(
      'jobrun_id', jobrun_id);

    return this.http.get<IJoblogsRecords>(
      this.joblogByIdUrl,
             { params: params }
    );

  }


  runJobByJobRunId(job_id: string, jobrun_id: string) {
    let params = new HttpParams().set(
      'job_id', job_id).set(
      'jobrun_id', jobrun_id);

    return this.http.get<IJoblogsRecords>(
      this.jobrunByJobRunIdUrl,
             { params: params }
    );

  }

  downloadLog(jobrun_id: string): Observable<Blob> {

    const params = new HttpParams().set(
      'jobrun_id', jobrun_id);
      const options = {params, responseType: 'blob' as 'json'};

    return this.http.get<Blob>(
      this.downloadlogUrl, options
    );


  }


}
