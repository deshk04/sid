import { Component, OnInit } from '@angular/core';
import {
  EventEmitter,
  Input,
  OnChanges,
  Output,
  ChangeDetectorRef,
} from '@angular/core';
import { SimpleChanges } from '@angular/core';

import { Router, ActivatedRoute } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';
import { SchedulesService } from '../../services/schedules.service';
import { IScheduleSelect, initScheduleRecord, IScheduleConfig } from '../../models/schedule';
import { JobsService } from '../../services/jobs.service';

import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { IJob } from 'src/app/models/jobs';

export interface IScheduleJob {
  job_id: number;
  job_name: string;
  run_type: string;
}
export interface IdayOfMonth {
  day: string;
  value: string;
}

type jobScheduleType = Record<number, Array<IScheduleJob>>;

@Component({
  selector: 'editschedule',
  templateUrl: './editschedule.component.html',
  styleUrls: ['./editschedule.component.css'],
})
export class EditscheduleComponent implements OnInit {
  // schedule: IScheduleSelect;
  schedule: IScheduleSelect = JSON.parse(JSON.stringify(initScheduleRecord));
  origSchedule: IScheduleSelect;

  currjobSchedule: jobScheduleType = {};
  schdataloaded: boolean = false;
  jobsdataloaded: boolean = false;

  schedule_id: number;
  ctype: string;
  cloneSchFlag: boolean = false;
  newScheduleFlag: boolean = false;

  jobRecords: Array<IJob> = [];

  // filteredObjects: IJob[];
  dailydays = {
    monday: false,
    tuesday: false,
    wednesday: false,
    thursday: false,
    friday: false,
    saturday: false,
    sunday: false,
  };
  dayofmonth: IdayOfMonth[] = [
    { day: '1', value: '1st day' },
    { day: '2', value: '2nd day' },
    { day: '3', value: '3rd day' },
    { day: '4', value: '4th day' },
    { day: '5', value: '5th day' },
    { day: '6', value: '6th day' },
    { day: '7', value: '7th day' },
    { day: '8', value: '8th day' },
    { day: '9', value: '9th day' },
    { day: '10', value: '10th day' },
    { day: '11', value: '11th day' },
    { day: '12', value: '12th day' },
    { day: '13', value: '13th day' },
    { day: '14', value: '14th day' },
    { day: '15', value: '15th day' },
    { day: '16', value: '16th day' },
    { day: '17', value: '17th day' },
    { day: '18', value: '18th day' },
    { day: '19', value: '19th day' },
    { day: '20', value: '20th day' },
    { day: '21', value: '21st day' },
    { day: '22', value: '22nd day' },
    { day: '23', value: '23rd day' },
    { day: '24', value: '24th day' },
    { day: '25', value: '25th day' },
    { day: '26', value: '26th day' },
    { day: '27', value: '27th day' },
    { day: '28', value: '28th day' },
    { day: '29', value: '29th day' },
    { day: '30', value: '30th day' },
    { day: '31', value: '31st day' },
    { day: '0', value: 'Last day of month' },
  ];
  // dayofmth: number = 1;
  dimhour: number[] = [];
  dimmin: number[] = [];
  // hour = 0;
  // min = 0;

  constructor(
    private _loadingService: TdLoadingService,
    private schedulesService: SchedulesService,
    private router: Router,
    private route: ActivatedRoute,
    private jobsService: JobsService,
    private sidSnackbarComponent: SidSnackbarComponent,
    private _changeDetectorRef: ChangeDetectorRef
  ) {
    this.schedule_id = this.route.snapshot.params['id'];
    this.ctype = this.route.snapshot.params['type'];

    if (this.ctype && this.ctype == 'c') {
      this.cloneSchFlag = true;
    }
    var i;
    for (i = 0; i < 24; i++) {
      this.dimhour.push(i.toString());
    }
    for (i = 0; i < 60; i++) {
      this.dimmin.push(i.toString());
    }

    this.setSchedule();
  }

  ngOnInit(): void { }
  getJobs() {
    this._loadingService.register('loadingeditschsid');

    this.jobsService.getJobs().subscribe(
      result => {
        this._loadingService.resolve('loadingeditschsid');
        if (result.status != 'ok') {
          this.sidSnackbarComponent.showMessage('No jobs founds, please add job first');
          return;
        }
        this.jobRecords = result.records.jobs;
        this.jobsdataloaded = true;
        // this.filterObjects('');

        this._changeDetectorRef.detectChanges();
      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingeditschsid');
        this.sidSnackbarComponent.systemError();

      })
  }

  setSchedule() {
    this.newScheduleFlag = false;
    this.getJobs();
    if (this.schedule_id < 1) {
      this.newScheduleFlag = true;
      this.origSchedule = JSON.parse(JSON.stringify(this.schedule));
      this.schdataloaded = true;
      this.init();
    } else {
      this.getSchedule();
    }
  }
  init() {
    this.currjobSchedule = {};
    this.schedule.scheduleconfig.forEach((element) => {
      let sjob: IScheduleJob = {
        job_id: element.job_id,
        job_name: element.job_name,
        run_type: element.run_type,
      };
      if (this.currjobSchedule[element.job_sequence] == null) {
        this.currjobSchedule[element.job_sequence] = [sjob];
      } else {
        let jobs = this.currjobSchedule[element.job_sequence];
        if (!jobs.some((elm) => elm.job_id === sjob.job_id)) {
          jobs.push(sjob);
        }
        this.currjobSchedule[element.job_sequence] = jobs;
      }
    });
    if (this.schedule.schedules.frequency !== null) {
      if (this.schedule.schedules.frequency.toLowerCase() === 'monthly') {
        // this.frequency = 'M';
      } else {
        // this.frequency = 'D';
        if (this.schedule.schedules.day_of_week !== null) {
          var days = this.schedule.schedules.day_of_week.split(',');
          days.forEach((day) => {
            switch (day) {
              case '0':
                this.dailydays['sunday'] = true;
                break;
              case '1':
                this.dailydays['monday'] = true;
                break;
              case '2':
                this.dailydays['tuesday'] = true;
                break;
              case '3':
                this.dailydays['wednesday'] = true;
                break;
              case '4':
                this.dailydays['thursday'] = true;
                break;
              case '5':
                this.dailydays['friday'] = true;
                break;
              case '6':
                this.dailydays['saturday'] = true;
                break;
            }
          });
        }
      }
    } else {
      this.schedule.schedules.frequency = 'Daily';
    }

  }

  getSchedule() {
    this._loadingService.register('loadingeditschsid');

    this.schedulesService.getScheduleById(String(this.schedule_id)).subscribe(
      (result) => {
        this._loadingService.resolve('loadingeditschsid');
        if (result.status != 'ok') {
          this.sidSnackbarComponent.showMessage(result.message);
          return;
        }
        this.schedule = result.records;
        if (this.cloneSchFlag) {
          this.schedule.schedules.id = -1;
          this.schedule.schedules.schedule_name = '';
          this.schedule_id = -1;
        }
        this.origSchedule = JSON.parse(JSON.stringify(this.schedule));
        this.init();
        this.schdataloaded = true;
        this._changeDetectorRef.detectChanges();
      },
      (err) => {
        console.log(err);
        this._loadingService.resolve('loadingeditschsid');
        this.sidSnackbarComponent.systemError();
      }
    );
  }

  handleAdd(event, step) {
    // console.log(this.currjobSchedule);
  }
  handleRemove(event, step) {
    //    delete this.currjobSchedule[step];
  }

  // filterObjects(value): void {
  //   console.log('in filteredobject');
  //   console.log(value);
  //   this.filteredObjects = this.jobRecords.filter((obj: any) => {
  //     if (value) {
  //       return obj.job_name.toLowerCase().indexOf(value.toLowerCase()) > -1;
  //     } else {
  //       return false;
  //     }
  //   });
  //   // .filter((filteredObj: any) => {
  //   //   return this.jobRecords ? this.jobRecords.indexOf(filteredObj) < 0 : true;
  //   // });
  // }

  deleteStep(stepNum) {
    delete this.currjobSchedule[stepNum];
    let keys = Object.keys(this.currjobSchedule).map((key) => parseInt(key));
    //this.currjobSchedule
    let tempJobSchedule: jobScheduleType = {};

    keys.forEach((element) => {
      if (element > stepNum) {
        tempJobSchedule[element - 1] = this.currjobSchedule[element];
      } else {
        tempJobSchedule[element] = this.currjobSchedule[element];
      }
    });
    this.currjobSchedule = tempJobSchedule;
  }

  addStep() {
    let keys = Object.keys(this.currjobSchedule).map((key) => parseInt(key));
    if (keys !== null && keys.length > 0) {
      let maxkey = keys[keys.length - 1] + 1;
      this.currjobSchedule[maxkey] = [];
    } else {
      this.currjobSchedule[1] = [];
    }
  }
  buildSchedule() {
    // add the steps
    let keys = Object.keys(this.currjobSchedule).map((key) => parseInt(key));
    this.schedule.scheduleconfig = [];
    keys.forEach((step) => {
      this.currjobSchedule[step].forEach(
        (job) => {
          let sch: IScheduleConfig = {
            id: this.schedule_id,
            job_id: job.job_id,
            job_sequence: step,
            job_name: job.job_name,
            run_type: job.run_type
          }
          this.schedule.scheduleconfig.push(sch)
        }
      );
    });
    // add frequency
    if (this.schedule.schedules.frequency === 'Daily') {
      let days = [];
      let wdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
      let i = 0
      wdays.forEach(
        day => {
          if (this.dailydays[day] == true) {
            days.push(i.toString())
          }
          i = i + 1;
        }
      )
      this.schedule.schedules.day_of_week = days.join(',')
    }

  }
  validate() {

    // check if schedule details are populated
    let messages = []
    if (this.schedule.schedules.schedule_name == '' ||
      this.schedule.schedules.schedule_name.toLowerCase() == 'new') {
      messages.push('Invalid Schedule Name');
    }
    if (this.schedule.schedules.frequency == '' ||
      !['Daily', 'Monthly'].includes(this.schedule.schedules.frequency)) {
      messages.push('Invalid Frequency');
    }
    if (this.schedule.schedules.frequency == 'Daily' &&
    (this.schedule.schedules.day_of_week == null ||
    this.schedule.schedules.day_of_week.trim() == '')){
      messages.push('Invalid Daily Frequency');
    }
    if (this.schedule.schedules.frequency !== 'Daily' &&
    (this.schedule.schedules.day_of_month == null ||
    this.schedule.schedules.day_of_month.trim() == '')){
      messages.push('Invalid Monthly Frequency');
    }
    if (this.schedule.schedules.hours == null ||
    this.schedule.schedules.hours.trim() == ''){
      messages.push('Invalid Frequency time');
    }

      // check if the schedule config (jobs) are populated
    if(this.schedule.scheduleconfig == null ||
      this.schedule.scheduleconfig.length == 0){
        messages.push('Invalid Steps');
      }
    else{
      let keys = Object.keys(this.currjobSchedule).map((key) => parseInt(key));
      keys.forEach((step) => {
        if(this.currjobSchedule[step] == null ||
          this.currjobSchedule[step].length == 0 ){
          messages.push('Invalid step: '.concat(step.toString()));
        }
      });

    }
    if(messages.length > 0){
      this.sidSnackbarComponent.showMessage(messages);
      return false;
    }


    return true;
  }
  submit() {
    this.buildSchedule();

    if (!this.validate()) {
      console.log('error');
      return;
    }
    this._loadingService.register('loadingeditschsid');
    // console.log(this.schedule);

    this.schedulesService.updateSchedule(this.schedule).subscribe(
      (result) => {
        if (result.status != 'ok') {
          this.sidSnackbarComponent.showMessage(result.message);
          this._loadingService.resolve('loadingeditschsid');
          return;
        }
        this.schedule = result.records;
        this.origSchedule = JSON.parse(JSON.stringify(this.schedule));

        this._loadingService.resolve('loadingeditschsid');
        this.sidSnackbarComponent.parseResult(result);
      },
      (err) => {
        console.log(err);
        this._loadingService.resolve('loadingeditschsid');
        this.sidSnackbarComponent.systemError();
      }
    );


  }
  resetSchedule() {

    if (this.schedule_id < 1 && this.cloneSchFlag == false) {
      this.schedule = JSON.parse(JSON.stringify(initScheduleRecord));
    } else {
      this.schedule = JSON.parse(JSON.stringify(this.origSchedule));
    }
    this.init();
  }
  returnSchedule() {
    if (this.schedule_id > 0) {
      console.log('go to details');
      this.router.navigate(['/scheduledetails', this.schedule_id]);

    }

  }
}
