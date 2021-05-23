import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms'; // new add
import { FormControl } from '@angular/forms';

import { TdLoadingService } from '@covalent/core/loading';

import { ConnectionsService } from '../../services/connections.service';
import { ISFConnector } from '../../models/salesforce';
import { IConnectorDetails } from '../../models/connection';
import { IDimSystemTypes } from '../../models/dimensions';
import { DimensionDataService } from '../../data/dimensiondata.service';
import { JobsService } from '../../services/jobs.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'salesforce-connection',
  templateUrl: './salesforce.component.html',
  styleUrls: ['./salesforce.component.css']
})
export class SalesforceComponent implements OnInit {

  @Input()
  connector: IConnectorDetails;

  @Output('close')
  closeflag: EventEmitter<boolean> = new EventEmitter<boolean>();

  queryType = 'new';
  sfconnector: ISFConnector;
  connectionForm: FormGroup; // new form fields
  dataloaded = false;
  hasError = false;
  showForm = true;
  dimSystemTypes: Array<IDimSystemTypes>;

  constructor(
    private _loadingService: TdLoadingService,
    private fb: FormBuilder,
    private connectionService: ConnectionsService,
    private dimensionDataService: DimensionDataService,
    private jobsService: JobsService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {
    // this.showForm = true;
    this.getDimensions();
    this.createConnectorForm();
    this.patchForm();
  }

  ngOnInit(): void {
    // console.log(this.connector);
    if (this.connector) {
      this.patchForm()
    }

  }

  createConnectorForm() {
    this.connectionForm = this.fb.group({
      query_type: [{ value: 'new', disabled: false }, [Validators.required]],
      conn_id: [{ value: -1, disabled: false }],
      name: [{ value: '', disabled: false }, [Validators.required]],
      conn_type: [{ value: 'Salesforce', disabled: false }, [Validators.required]],
      conn_system_type: [{ value: '', disabled: false }, [Validators.required]],
      auth_username: [{ value: '', disabled: false }, [Validators.required]],
      auth_password: [{ value: '', disabled: false }, [Validators.required]],
      security_token: [{ value: '', disabled: false }, [Validators.required]],
      auth_host: [{ value: '', disabled: false }],
      oauth_key: [{ value: '', disabled: false }],

    })
  }
  patchForm() {
    // patch data from this.connector
    if (this.connector != null) {
      this.connectionForm.patchValue({
        conn_id: this.connector.conn_id,
        name: this.connector.name,
        conn_type: 'Salesforce',
        conn_system_type: this.connector.conn_system_type,
        auth_username: this.connector.sfauth.auth_username,
        auth_host: this.connector.sfauth.auth_host,
        auth_password: this.connector.sfauth.auth_password,
        security_token: this.connector.sfauth.security_token
      })
      if (this.connector.query_type){
        this.connectionForm.patchValue({
          query_type: this.connector.query_type
        })
      }
    }
    this.showForm = true;
    // console.log(this.connectionForm);
    // console.log(this.connector);

  }
  getDimensions(){
    this._loadingService.register('loadingsiddimconn');

    this.dimensionDataService.dimensionRecord.subscribe(
      result => {
        this._loadingService.resolve('loadingsiddimconn')
        this.dimSystemTypes = result.records.dimsystemtypes;
        this.dataloaded = true;

      }
    )
  }
  onSubmit(){
    let msg = 'Record Saved';
    if(this.connectionForm.invalid){
      this.sidSnackbarComponent.showMessage('Invalid Form: Please fill the highlighted fields');
      return
    }

    this._loadingService.register('loadingsiddimconn');

    this.connectionService.updateConnection(
      this.connectionForm
    ).subscribe(
      result => {
        this._loadingService.resolve('loadingsiddimconn')
        this.sidSnackbarComponent.showMessage(result.message);

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsiddimconn');
        this.sidSnackbarComponent.systemError();

      })

  }

  onCancel(){
    this.showForm = false;
    this.closeflag.emit(true);
  }

   toggleSensitiveField(fieldName) {
    var field = (<HTMLInputElement>document.getElementById(fieldName));
    if (field.type === "password") {
      field.type = "text";
    } else {
      field.type = "password";
    }
  }

  refreshModels() {
    if (!this.connector){
      return;
    }
    this._loadingService.register('loadingsiddimconn');

    this.jobsService
      .getConnModels(
        String(this.connector.conn_id),
        null
      )
      .subscribe(
        (result) => {
          this._loadingService.resolve('loadingsiddimconn');
          if(result.status == 'ok') {
            this.sidSnackbarComponent.showMessage('Metadata refreshed', true);
          }
          else{
            this.sidSnackbarComponent.showMessage(result.message);
          }
        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsiddimconn');
          this.sidSnackbarComponent.systemError();

        }
      );
  }


}
