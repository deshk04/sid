import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FormControl } from '@angular/forms';

import { TdLoadingService } from '@covalent/core/loading';
import { Router, ActivatedRoute } from '@angular/router';

import { JobsService } from '../../services/jobs.service';
import { DimensionDataService } from '../../data/dimensiondata.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { IConnectorDetails } from '../../models/connection';
import { IDimRef } from '../../models/dimensions';

import {
  IJob,
  IJobModels,
  IJobFields,
  IJobconfig,
  initJobRecord
} from '../../models/jobs';
import * as moment from 'moment';

@Component({
  selector: 'app-editjob',
  templateUrl: './editjob.component.html',
  styleUrls: ['./editjob.component.css']
})
export class EditjobComponent implements OnInit {

  errorMessages = [];
  job_id: number;
  ptype: string;
  jstep = 1;
  // seletedJobRecord details
  selectedJobRecord: IJob = JSON.parse(JSON.stringify(initJobRecord));
  origJobRecord: IJob;

  showSelectedMapRecord: boolean = false;
  newJobFlag = false;
  cloneJobFlag = false;
  adhocJobFlag = false;
  dimRef: IDimRef;


  // initialize conn record
  selectedConnRecord: IConnectorDetails = {
    conn_id: -1,
    conn_system_type: '',
    conn_type: '',
    name: '',
    conn_logo: '',
    create_date: '',
    modified_date: '',
    query_type: 'update',

    sfauth: {
      auth_username: '',
      auth_password: '',
      auth_host: '',
      oauth_object_id: '',
      security_token: '',
    },
    s3auth: {
      aws_access_key_id: '',
      aws_secret_access_key: '',
      bucket_name: '',
      aws_region: '',
    },
  };

  dataloadedflag = false;

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private router: Router,
    private route: ActivatedRoute,
    private _formBuilder: FormBuilder,
    private _loadingService: TdLoadingService,
    private jobsService: JobsService,
    private dimensionDataService: DimensionDataService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {

    this.job_id = this.route.snapshot.params['id'];
    this.ptype = this.route.snapshot.params['type'];

    if (this.ptype && this.ptype == 'c') {
      this.cloneJobFlag = true
    }
    this.selectedJob();
  }

  ngOnInit(): void {
//    console.log(this.route.snapshot);
  }


  selectedJob() {
    this.newJobFlag = false;
    if (this.job_id < 1) {
      this.newJobFlag = true;
    }
    this.origJobRecord = JSON.parse(JSON.stringify(this.selectedJobRecord));

    this._loadingService.register('loadingsideditjob');

    if (this.newJobFlag) {
      // new job
      // this.selectedJobRecord = event;
      this.dataloadedflag = true;
      this._loadingService.resolve('loadingsideditjob');
    } else {
      // existing job
      this.jobsService.getJobbyId(String(this.job_id)).subscribe(
        (result) => {
          if (this.cloneJobFlag) {
            result.records.jobs[0].job_id = -1;
            result.records.jobs[0].job_name = '';
          }
          // this.selectedJobRecord = result.records.jobs[0];
          this.selectedJobRecord = JSON.parse(JSON.stringify(result.records.jobs[0]));

          this.origJobRecord = JSON.parse(JSON.stringify(this.selectedJobRecord));
          if(this.selectedJobRecord.run_type == 'A') {
            this.adhocJobFlag = true;
          }
          else{
            this.adhocJobFlag = false;
          }

          this.dataloadedflag = true;
          this._loadingService.resolve('loadingsideditjob');
        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsideditjob');
          this.sidSnackbarComponent.systemError();
        }
      );
    }

  }

  sourceDetails(sourceStatus: boolean) {
    this._loadingService.register('loadingsideditjob');

    if(sourceStatus){
      this.jstep = 2;
    }
    this._loadingService.resolve('loadingsideditjob');

  }


  DestinationDetails(destStatus: boolean) {
    this._loadingService.register('loadingsideditjob');

    // console.log('dest ended');
    if(destStatus){
      if (this.selectedJobRecord.dest_config.conn_type != 'Salesforce'){
        this.selectedJobRecord.destfields = this.selectedJobRecord.sourcefields;
      }
      if(this.adhocJobFlag){
        /* if the job type is adhoc
          then we dont go to mapping step instead we
          go to final step
        */
        this.jstep = 4;
      }
      else{
        /*
          go to mapping step
        */
        this.jstep = 3;
      }
    }
    else{
      if(!this.adhocJobFlag){
        /*
          go to source connector step
        */
        this.jstep = 1;
      }
    }
    this._loadingService.resolve('loadingsideditjob');

  }
  mapDetails(mapStatus: boolean) {
    if(mapStatus){
      this.jstep = 4;
    }
    else {
      this.jstep = 2;
    }
  }
  adhocJobToggle(event){
    if(this.adhocJobFlag){
      this.selectedJobRecord.run_type = 'A'
    }
    else{
      this.selectedJobRecord.run_type = 'R'
    }
  }

  resetJob(){
    if(this.job_id < 1){
      // we have to deep copy, simpel assignment wont work
      // as we have deep interface
      this.selectedJobRecord = JSON.parse(JSON.stringify(initJobRecord));
    }
    else{
      this.selectedJobRecord = JSON.parse(JSON.stringify(this.origJobRecord));
    }
    this.jstep = 1;
  }

  validateJob(){
    let errorMessage = [];
    if(this.selectedJobRecord.job_name == null ||
      this.selectedJobRecord.job_name == '' ||
      this.selectedJobRecord.job_name == 'New') {
      errorMessage.push('Invalid Job name');
    }

    if(this.selectedJobRecord.run_type == 'A'){
      if(this.selectedJobRecord.dest_config == null ||
        this.selectedJobRecord.dest_config.conn_id < 1) {
        errorMessage.push('Invalid Connector');
      }
    }

    if(errorMessage.length > 0){
      this.sidSnackbarComponent.showMessage(errorMessage);
      return false;
    }

    return true;
  }

  createForm(){

  }

  submitForm(){


    // validate the job
    if(!this.validateJob()){
      return;
    }
    this._loadingService.register('loadingsidjob');

    this.jobsService.updateJob(this.selectedJobRecord).subscribe(
      (result) => {
        this._loadingService.resolve('loadingsidjob');
        this.sidSnackbarComponent.parseResult(result);

      },
      (err) => {
        console.log(err);
        this._loadingService.resolve('loadingsidjob');
        this.sidSnackbarComponent.systemError();
      }
    );

  }
  cancel(){
    this.jstep = 3;
  }

}
