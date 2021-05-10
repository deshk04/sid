import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IScheduleRecords, IScheduleLogRecords, IScheduleRecordById } from '../models/schedule';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SchedulesService {
  private scheduleUrl = HOST_API + 'getschedules/';  // URL to web API
  private runScheduleUrl = HOST_API + 'runschedule/';  // URL to web API
  private getScheduleLogUrl = HOST_API + 'getschedulelogs/';  // URL to web API
  private getScheduleByIdUrl = HOST_API + 'getschedulebyid/';  // URL to web API
  private updateScheduleUrl = HOST_API + 'updateschedule/';  // URL to web API

  constructor(private http: HttpClient) { }

  getSchedules() {
    //    let params = new HttpParams().set('query', queryString);

    return this.http.get<IScheduleRecords>(
      this.scheduleUrl,
      //        { params: params }
    );

  }
  runSchedule(schedule_id: string, rundate: string, markcomplete: string) {
    let params = new HttpParams().set(
      'schedule_id', schedule_id).set(
      'rundate', rundate).set(
      'markcomplete', markcomplete)

    return this.http.get<IScheduleRecords>(
      this.runScheduleUrl,
             { params: params }
    );

  }

  getScheduleLog(schedule_id: string, startDate: string, endDate: string) {
    let params = new HttpParams().set(
      'schedule_id', schedule_id).set(
        'startdate', startDate).set('enddate', endDate);

    return this.http.get<IScheduleLogRecords>(
      this.getScheduleLogUrl,
             { params: params }
    );

  }

  getScheduleById(schedule_id: string) {
    let params = new HttpParams().set(
      'schedule_id', schedule_id);

    return this.http.get<IScheduleRecordById>(
      this.getScheduleByIdUrl,
             { params: params }
    );
  }

  /* Post method */
  updateSchedule(data: any): Observable<any> {
    const formData: FormData = new FormData();
    var postData = JSON.stringify(data);
    formData.append('data', postData);

    return this.http.post<IScheduleRecordById>(
        this.updateScheduleUrl,
        formData
    );
  }


}
