import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms'; // new add
import { FormControl } from '@angular/forms';

import { TdLoadingService } from '@covalent/core/loading';

import { ConnectionsService } from '../../services/connections.service';
import { IS3Connector } from '../../models/awss3';
import { IConnectors, IConnectorDetails } from '../../models/connection';
import { IDimSystemTypes } from '../../models/dimensions';
import { DimensionDataService } from '../../data/dimensiondata.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
@Component({
  selector: 'awss3-connection',
  templateUrl: './awss3.component.html',
  styleUrls: ['./awss3.component.css']
})
export class Awss3Component implements OnInit {

  @Input()
  connector: IConnectorDetails;

  @Output('close')
  closeflag: EventEmitter<boolean> = new EventEmitter<boolean>();

  queryType = 'new';
  s3connector: IS3Connector;
  connectionForm: FormGroup; // new form fields
  errorFlag: boolean = false;
  dataloaded = false;
  showForm = true;
  dimSystemTypes: Array<IDimSystemTypes>;

  constructor(
    private _loadingService: TdLoadingService,
    private fb: FormBuilder,
    private connectionService: ConnectionsService,
    private dimensionDataService: DimensionDataService,
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
      conn_type: [{ value: 'AWS_S3', disabled: false }, [Validators.required]],
      conn_system_type: [{ value: '', disabled: false }, [Validators.required]],
      aws_access_key_id: [{ value: '', disabled: false }, [Validators.required]],
      aws_secret_access_key: [{ value: '', disabled: false }, [Validators.required]],
      bucket_name: [{ value: '', disabled: false }, [Validators.required]],
      aws_region: [{ value: '', disabled: false }, [Validators.required]],

    })
  }
  patchForm() {
    // patch data from this.connector
    if (this.connector != null) {
      this.connectionForm.patchValue({
        conn_id: this.connector.conn_id,
        name: this.connector.name,
        conn_type: 'AWS_S3',
        conn_system_type: this.connector.conn_system_type,
        aws_access_key_id: this.connector.s3auth.aws_access_key_id,
        aws_secret_access_key: this.connector.s3auth.aws_secret_access_key,
        bucket_name: this.connector.s3auth.bucket_name,
        aws_region: this.connector.s3auth.aws_region
      })
      if (this.connector.query_type){
        this.connectionForm.patchValue({
          query_type: this.connector.query_type
        })
      }
    }
    this.showForm = true;
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


}
