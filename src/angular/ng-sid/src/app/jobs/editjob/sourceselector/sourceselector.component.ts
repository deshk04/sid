import { Component, EventEmitter, Input, OnChanges, Output, ChangeDetectorRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { SimpleChanges } from '@angular/core';

import { Router } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';

import { IJob, IJobFields, IJobModels , IJobquery } from '../../../models/jobs';
import { IConnectorDetails } from '../../../models/connection';
import { DimensionDataService } from '../../../data/dimensiondata.service';
import { DocumentService } from '../../../services/document.service';
import { IDocumentRecord } from '../../../models/documents';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { JobsService } from '../../../services/jobs.service';
import { from } from 'rxjs';
import { IDimRef } from '../../../models/dimensions';
import { ISFParsedQuery, initsfjob } from '../../../models/salesforce';

@Component({
  selector: 'sourceselector',
  templateUrl: './sourceselector.component.html',
  styleUrls: ['./sourceselector.component.css']
})
export class SourceselectorComponent implements OnChanges {

  files: any;
  dataloaded: boolean = false;
  editFlag: boolean = false;
  connChangedFlag: boolean = false;

  disabled: boolean = false;
  enabled: boolean = true;
  dimRef: IDimRef;

  delimiter: string = '|';
  newline: string = 'LF';
  sfjob: ISFParsedQuery = JSON.parse(JSON.stringify(initsfjob));

  sourceConnector: IConnectorDetails = {
    conn_id: -1,
    name: '',
    conn_type: '',
    conn_system_type: '',
    conn_logo: '',
    create_date: '',
    modified_date: '',
    query_type: '',
    sfauth: null,
    s3auth: null

  }

  @Input()
  job: IJob;

  @Output()
  ostatus: EventEmitter<boolean> = new EventEmitter<boolean>();

  sfdataloaded = false;

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _loadingService: TdLoadingService,
    private router: Router,
    private dimensionDataService: DimensionDataService,
    private documentService: DocumentService,
    private jobsService: JobsService,
    private sidSnackbarComponent: SidSnackbarComponent
    ) {
      // this.getDimensions();
  }

  // ngOnInit(): void {
  //   this.init();
  //   this.getDimensions();
  //   // this.dataloaded = true;
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

    this.init();
    this.getDimensions();
  }

  init(){
    this.connChangedFlag = false;
    this.sfjob.filter = 'Y';
  }
  selectedConnection(connector: IConnectorDetails) {
    this.connChangedFlag = true;
    this.sfdataloaded = false;
    // this.sourceConnector = connector;
    this.job.source_config.conn_id = connector.conn_id;
    this.job.source_config.conn_name  = connector.name;
    this.job.source_config.conn_logo_path  = connector.conn_logo;
    this.job.source_config.conn_system_type  = connector.conn_system_type;
    this.job.source_config.conn_type = connector.conn_type;

    if(connector.conn_type == 'Salesforce'){
//      this.fetchSfModels(null);
      this.sfjob.connector = connector;
      this.sfjob.query = this.job.source_config.query;
      this.sfdataloaded = true;

    }
  }

  getDimensions() {
    this._loadingService.register('loadingsourcesid');
    this.dimensionDataService.dimensionRecord.subscribe((result) => {
      this._loadingService.resolve('loadingsourcesid');
      if (result.records) {
        this.dimRef = result.records;
        this.dataloaded = true;
      }
    });
  }


  selectedS3File(filename: string) {

    this._loadingService.register('loadingsourcesid');

    this.documentService.s3Document(
      this.job.source_config.conn_id.toString(),
      filename,
      this.delimiter,
      this.newline
      ).subscribe(
      (result) => {
        if (result.status == 'ok'){
          if(result.records.document.length > 0) {
            this.job.sourcefields

            this.job.sourcefields = result.records.document;
            // this.job.source_config = result.records.config;
            this.job.source_config.filestartwith = result.records.config.filestartwith
            this.job.source_config.fileendwith = result.records.config.fileendwith
            this.job.source_config.delimiter = result.records.config.delimiter
            this.job.source_config.lineterminator = result.records.config.lineterminator
            this.job.source_config.encoding = result.records.config.encoding
            this.job.source_config.filepath = result.records.config.filepath

            this.job.sourcefields.forEach(function (element) {
              element.model_name  = result.records.config.filestartwith;
            });

          }
          else {
            this.sidSnackbarComponent.showMessage('fields not found');

          }
        }
        else{
          console.log('error');
 //         this._matSnackBar.open(result.message, 'Dismiss', this.msgConfig);
        }
        this._loadingService.resolve('loadingsourcesid');
      },
      (err) => {
        console.log(err);
        this._loadingService.resolve('loadingsourcesid');
        this.sidSnackbarComponent.systemError();

      }
      );


  }

  selectLocalFile(event) {

  }
  uploadLocalFile() {

    this._loadingService.register('loadingsourcesid');

    this.documentService.postDocument(
      this.files,
      this.delimiter,
      this.newline
      ).subscribe(
      (result) => {
        // console.log(result);
        if (result.status == 'ok'){
          if(result.records.document.length > 0) {
            this.job.sourcefields = result.records.document;
            this.job.source_config.filestartwith = result.records.config.filestartwith
            this.job.source_config.fileendwith = result.records.config.fileendwith
            this.job.source_config.delimiter = result.records.config.delimiter
            this.job.source_config.lineterminator = result.records.config.lineterminator
            this.job.source_config.encoding = result.records.config.encoding
            this.job.source_config.filepath = 'local'

            this.job.sourcefields.forEach(function (element) {
              element.model_name  = result.records.config.filestartwith;
            });
            this.editFlag = false;
          }
          else {
            this.sidSnackbarComponent.showMessage('fields not found');
          }
        }
        else{
          console.log('error');
//          this._matSnackBar.open(result.message, 'Dismiss', this.msgConfig);
        }
        this._loadingService.resolve('loadingsourcesid');
      },
      (err) => {
        console.log(err);
        this._loadingService.resolve('loadingsourcesid');
        this.sidSnackbarComponent.systemError();

      }
      );

  }

  SfQuery(event){
    this.job.sourcefields = this.sfjob.fields;
    this.job.source_config.model = this.sfjob.model_name;
    this.sidSnackbarComponent.showMessage('Query Parsed successful, Please press Next', true);

    this.editFlag = false;
  }


  toggleEditFlag(){
    this.editFlag = !this.editFlag;
  }

  validate(){

    // console.log(this.job);

    let errorMessage = [];
    if(this.job.source_config == null) {
      errorMessage.push('Invalid source config');
    }
    else if(this.job.source_config.conn_id == null
      || this.job.source_config.conn_id < 1)
    {
      errorMessage.push('Invalid connector');
    }
    if(this.job.source_config.conn_type == 'File' ||
    this.job.source_config.conn_type == 'AWS_S3'){
      if(this.job.source_config.filestartwith == null ||
        this.job.source_config.filestartwith == ''){
          errorMessage.push('Invalid filename');
        }
        if(this.job.source_config.conn_type == 'AWS_S3' && (
          this.job.source_config.filepath == null ||
          this.job.source_config.filepath == '')){
            errorMessage.push('Invalid filepath');
          }
    }
    if(this.job.source_config.conn_type == 'Salesforce'){
      if(this.job.source_config.query.query == '' ||
      this.job.source_config.model == ''){
        errorMessage.push('Invalid query');
      }

    }
    if(this.job.sourcefields == null || this.job.sourcefields.length < 1) {
      errorMessage.push('Invalid fields')
    }

    if(errorMessage.length > 0){
      this.sidSnackbarComponent.showMessage(errorMessage);
      return false;
    }
    return true;

  }

  submit(){
    if(this.validate()){
      this.ostatus.emit(true);
    }

  }
}
