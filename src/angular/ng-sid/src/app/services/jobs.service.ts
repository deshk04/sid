import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IJobsRecords, IJobModelRecords } from '../models/jobs';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JobsService {
  private jobsUrl = HOST_API + 'getjobs/';
  private jobsByIdUrl = HOST_API + 'getjobbyid/';
  private jobrunByIdUrl = HOST_API + 'runjobbyid/';
  private getConnModelsUrl = HOST_API + 'getconnmodels/';
  private fetchConnModelsUrl = HOST_API + 'fetchconnmodels/';
  private updateJobUrl = HOST_API + 'updatejob/';
  private jobrunByFileUrl = HOST_API + 'runjobbyfile/';
  private jobsListUrl = HOST_API + 'getjobslist/';

  constructor(private http: HttpClient) { }

  getJobs() {
    //    let params = new HttpParams().set('query', queryString);

    return this.http.get<IJobsRecords>(
      this.jobsUrl,
      //        { params: params }
    );

  }

  getJobbyId(job_id: string) {
       let params = new HttpParams().set('job_id', job_id);

    return this.http.get<IJobsRecords>(
      this.jobsByIdUrl,
             { params: params }
    );

  }

  runJobById(job_id: string, rundate: string) {
    let params = new HttpParams().set(
      'job_id', job_id).set(
      'rundate', rundate);

    return this.http.get<IJobsRecords>(
      this.jobrunByIdUrl,
             { params: params }
    );

  }


  getConnModels(conn_id: string, model_name: string) {
    let params = new HttpParams().set(
      'conn_id', conn_id).set(
        'model_name', model_name
      );

    return this.http.get<IJobModelRecords>(
      this.getConnModelsUrl,
             { params: params }
    );

  }

  fetchConnModels(conn_id: string, model_name: string) {
    let params = new HttpParams().set(
      'conn_id', conn_id).set(
        'model_name', model_name
      );

    return this.http.get<IJobModelRecords>(
      this.fetchConnModelsUrl,
             { params: params }
    );

  }

  /* Post method */
  updateJob(data: any): Observable<any> {
    const formData: FormData = new FormData();
    var postData = JSON.stringify(data);
    formData.append('data', postData);

    return this.http.post<any>(
        this.updateJobUrl,
        formData
    );
  }

  runJobbyFile(job_id: string, fileToUpload: File, delimiter: string, lineterminator: string): Observable<IJobsRecords> {
    const formData: FormData = new FormData();
    formData.append('job_id', job_id);
    formData.append('document', fileToUpload, fileToUpload.name);
    formData.append('delimiter', delimiter);
    formData.append('lineterminator', lineterminator);

    return this.http.post<IJobsRecords>(
      this.jobrunByFileUrl,
      formData
    );

  }

}
