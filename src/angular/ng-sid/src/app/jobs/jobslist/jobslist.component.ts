import { Component, EventEmitter, Input, OnInit, Output, ChangeDetectorRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { Router } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';

import { JobsService } from '../../services/jobs.service';
import { IJobsRecords, IJob, initJobRecord } from '../../models/jobs';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'jobslist',
  templateUrl: './jobslist.component.html',
  styleUrls: ['./jobslist.component.css']
})
export class JobslistComponent implements OnInit {

  jobRecords: IJobsRecords;
  selectedJobRecord: IJob = initJobRecord;

  dataRecords: Array<IJob>;

  @Input()
  shownew: boolean = true;

  @Input()
  gridcomp: boolean = true;

  @Output()
  job: EventEmitter<IJob> = new EventEmitter<IJob>();

  dataloaded = false;
  errorMessage: string;

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _loadingService: TdLoadingService,
    private router: Router,
    private jobsService: JobsService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {

    this.getJobs();
  }

  ngOnInit(): void {

  }

  getJobs() {
    this._loadingService.register('loadingsid');

    this.jobsService.getJobs().subscribe(
      result => {
        this._loadingService.resolve('loadingsid')
        this.jobRecords = result;
        this.dataRecords = result.records.jobs;
        this.dataloaded = true;
        this._changeDetectorRef.detectChanges();

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsid');
        this.sidSnackbarComponent.systemError();

      })
  }


  newJob() {
    this.job.emit(this.selectedJobRecord);
  }

  editJob(job: IJob) {
    this.selectedJobRecord = job;
    this.job.emit(this.selectedJobRecord);
  }

  filterJobs(displayName: string = '') {

    this.dataRecords = this.jobRecords.records.jobs.filter(
      (obj) => {
        return obj.job_name.toLowerCase().indexOf(displayName.toLocaleLowerCase()) > -1;
      });


  }


}
