import { Component, EventEmitter, Input, OnInit, Output, ChangeDetectorRef, OnChanges } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SimpleChanges } from '@angular/core';

import { TdLoadingService } from '@covalent/core/loading';
import { IJob, IJobFields, IJobModels } from '../../../models/jobs';
import { IConnectorDetails } from '../../../models/connection';
import { DimensionDataService } from '../../../data/dimensiondata.service';
import { JobsService } from '../../../services/jobs.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { IDimRef } from '../../../models/dimensions';

@Component({
  selector: 'destselector',
  templateUrl: './destselector.component.html',
  styleUrls: ['./destselector.component.css']
})
export class DestselectorComponent implements OnChanges {

  files: any;
  dataloaded = false;
  editFlag = false;
  disabled: boolean = false;
  enabled: boolean = true;
  sfdataloaded: boolean = false;
  modelSelectedFlag: boolean = false;

  bulkCount: number[] = [];
  destModels: IJobModels[];
  destModelFields: IJobFields[];

  // transtype: string = 'insert';
  // upsertfield: string = '';
  // bulk_count: number = 1;

  dimRef: IDimRef;

  // filestartwith: string = '';
  // fileendwith: string = '.csv';
  // filepath: string = '';
  // filemask: string = '';
  // delimiter: string = '|';
  // lineterminator: string = 'LF';
  fileExt: string[] = ['.csv', '.json'];

  configForm: FormGroup;

  @Input()
  job: IJob;

  @Input()
  showprevious: boolean = true;

  @Output()
  ostatus: EventEmitter<boolean> = new EventEmitter<boolean>();

  errorMessage: string;

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _loadingService: TdLoadingService,
    private jobsService: JobsService,
    private sidSnackbarComponent: SidSnackbarComponent,
    private dimensionDataService: DimensionDataService,

  ) {
    this.sfdataloaded = false;
    this.getDimensions();

    this.bulkCount.push(1);
    var bnum = 50;
    while (bnum <= 2000) {
      this.bulkCount.push(bnum);
      bnum += 50;
    }

  }

  // ngOnInit(): void {
  //   this.destModelFields = this.job.destfields;
  //   this.destModels = this.job.models;
  //   this.dataloaded = true;
  //   this.editFlag = false;
  // }

  ngOnChanges(changes: SimpleChanges) {

    for (const propName in changes) {
      if (changes.hasOwnProperty(propName)) {
        switch (propName) {
          case 'job': {
            this.job = changes['job'].currentValue;
          }
        }
      }
    }
    this.destModelFields = this.job.destfields;
    this.destModels = this.job.models;

    this.getDimensions();
  }
  getDimensions() {
    this._loadingService.register('loadingsideditjob');
    this.dimensionDataService.dimensionRecord.subscribe((result) => {
      this._loadingService.resolve('loadingsideditjob');
      if (result.records) {
        this.dimRef = result.records;
        this.dataloaded = true;
        this.editFlag = false;

      }
    });
  }

  selectedConnection(connector: IConnectorDetails) {
    this.sfdataloaded = false;
    this.modelSelectedFlag = false;
    this.job.dest_config.conn_id = connector.conn_id;
    this.job.dest_config.conn_name = connector.name;
    this.job.dest_config.conn_logo_path = connector.conn_logo;
    this.job.dest_config.conn_system_type = connector.conn_system_type;
    this.job.dest_config.conn_type = connector.conn_type;

    if (connector.conn_type == 'Salesforce') {
      this.fetchSfModels(null);
    }

  }

  fetchSfModels(model_name) {
    this._loadingService.register('loadingdestsid');

    this.jobsService
      .fetchConnModels(
        String(this.job.dest_config.conn_id),
        model_name
      )
      .subscribe(
        (result) => {

          this.destModels = result.records.models;
          this.destModelFields = result.records.fields;
          this._changeDetectorRef.detectChanges();
          this.sfdataloaded = true;
          this._loadingService.resolve('loadingdestsid');

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingdestsid');
          this.sidSnackbarComponent.systemError();

        }
      );


  }

  modelChange(event) {
    this.fetchSfModels(this.job.dest_config.model);
    this.modelSelectedFlag = true;
  }

  validateInput() {
    let message = [];

    if(this.job.dest_config == null) {
      message.push('Invalid connector')
    }
    else if(this.job.dest_config.conn_id == null
      || this.job.dest_config.conn_id < 1)
    {
      message.push('Invalid connector');
    }
    else if (this.job.dest_config.conn_type == 'Salesforce') {
      if(this.job.dest_config.transaction_type == null ||
        this.job.dest_config.transaction_type == ''){
          message.push('Invalid Salesforce transaction type')
        }
      else if(this.job.dest_config.transaction_type == 'upsert' &&
      (this.job.dest_config.key_field == null ||
        this.job.dest_config.key_field == '')){
          message.push('Invalid Salesforce upsert key')
      }
    }
    else if (this.job.dest_config.conn_type == 'AWS_S3' ||
      this.job.dest_config.conn_type == 'File') {

      if (this.job.dest_config.filestartwith == '' || this.job.dest_config.filestartwith == null) {
        message.push('Filename is invalid')
      }
      if (this.job.dest_config.fileendwith == '' || this.job.dest_config.fileendwith == null) {
        message.push('File extension is invalid')
      }
      if (this.job.dest_config.conn_type == 'AWS_S3' &&
        (this.job.dest_config.filepath == '' || this.job.dest_config.filepath == null)) {
        message.push('Filepath is invalid')
      }

    }
    if (message.length > 0) {
      this.sidSnackbarComponent.showMessage(message);
      return false;
    }
    return true;
  }

  accept(ctype: string) {

    if (!this.validateInput()) {
      return
    }

    if (ctype == 'Salesforce') {
      this.job.destfields = this.destModelFields;
      this.job.models = this.destModels;
    }
    else {
      this.job.destfields = [];
      this.job.models = [];
      this.job.dest_config.model = this.job.dest_config.filestartwith;

    }
    this.editFlag = false;

  }
  submit() {
    if (!this.validateInput()) {
      return
    }
//    console.log('complete dest connector')

    this.ostatus.emit(true);

  }
  cancel(){
    this.ostatus.emit(false);
  }
  toggleEditFlag() {
    this.editFlag = !this.editFlag;
  }


}
