import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { FormGroup, Validators } from '@angular/forms';
import { FormControl } from '@angular/forms';
import { TdLoadingService } from '@covalent/core/loading';
import { Router, ActivatedRoute } from '@angular/router';

import { JobsService } from '../../services/jobs.service';
import { DimensionDataService } from '../../data/dimensiondata.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { IDimRef } from '../../models/dimensions';

import { IJob, initJobRecord } from '../../models/jobs';
import * as moment from 'moment';

@Component({
  selector: 'app-jobdetails',
  templateUrl: './jobdetails.component.html',
  styleUrls: ['./jobdetails.component.css']
})
export class JobdetailsComponent implements OnInit {

  job_id: number;
  dataloaded: boolean = false;
  // seletedJobRecord details
  selectedJobRecord: IJob = initJobRecord;

  files: any;
  cloneJobFlag = false;
  jobForm: FormGroup;
  updateFlag: boolean = true;
  oneoffFlag: boolean = false;

  currDate = new Date();
  jobRunDate = new FormControl(new Date(), Validators.required);

  delimiter: string = '|';
  newline: string = 'LF';
  dimRef: IDimRef;

  constructor(
    private _loadingService: TdLoadingService,
    private jobsService: JobsService,
    private dimensionDataService: DimensionDataService,
    private sidSnackbarComponent: SidSnackbarComponent,
    private route: ActivatedRoute,
    private router: Router,
    private _changeDetectorRef: ChangeDetectorRef,

    ) {
      this.job_id = this.route.snapshot.params['id'];
      this.dataloaded = false;
      this.getDimensions();
      this.selectedJob();
  }

  ngOnInit(): void { }

  getDimensions() {
    this._loadingService.register('loadingsidjob');
    this.dimensionDataService.dimensionRecord.subscribe((result) => {
      this._loadingService.resolve('loadingsidjob');
      if (result.records) {
        this.dimRef = result.records;
      }
    });
  }

  selectedJob() {
    this._loadingService.register('loadingsidjob');
    console.log(this.dataloaded);

      this.jobsService.getJobbyId(String(this.job_id)).subscribe(
        (result) => {
          this.selectedJobRecord = result.records.jobs[0];
          this._loadingService.resolve('loadingsidjob');
          this.dataloaded = true;
          console.log(this.dataloaded);
          console.log(this.selectedJobRecord);
          this._changeDetectorRef.detectChanges();

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsidjob');
          this.sidSnackbarComponent.systemError();

        }
      );
  }


  /*
    job run date
  */
  runJobByDate() {

    const runDate = moment(this.jobRunDate.value);
    if(this.selectedJobRecord.run_type == 'A'){
      this.sidSnackbarComponent.showMessage('Adhoc job run is not allowed from here');
      return
    }
    this._loadingService.register('loadingsidjob');

    this.jobsService.runJobById(
        String(this.job_id),
        String(runDate.valueOf())
      )
      .subscribe(
        (result) => {
          this._loadingService.resolve('loadingsidjob');
          this.sidSnackbarComponent.showMessage(result.message);

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsidjob');
          this.sidSnackbarComponent.systemError();

        }
      );
  }


  cloneJob() {
    this.router.navigate(['/editjob', this.job_id, 'c'])

  }
  editJob() {
    this.router.navigate(['/editjob', this.job_id, 'e'])

  }
  deleteJob() {

  }
  jobWithLocalFile(){

    this._loadingService.register('loadingsidjob');
    this.jobsService.runJobbyFile(
      String(this.job_id),
      this.files,
      this.delimiter,
      this.newline
      ).subscribe(
      (result) => {
          this.sidSnackbarComponent.showMessage(result.message);
         this._loadingService.resolve('loadingsidjob');
      },
      (err) => {
        console.log(err);
        this._loadingService.resolve('loadingsidjob');
        this.sidSnackbarComponent.systemError();

      }
    );

  }


}

