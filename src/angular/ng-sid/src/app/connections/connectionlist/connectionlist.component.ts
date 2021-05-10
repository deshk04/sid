import { Component, EventEmitter, OnInit, Input, Output, ChangeDetectorRef } from '@angular/core';

import { Router } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';

import { ConnectionsService } from '../../services/connections.service';
import { IConnectionRecords, IConnectors, IConnectorDetails, ISFAuth, IS3Auth } from '../../models/connection';
import { IDimConnectors } from '../../models/dimensions';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'connectionlist',
  templateUrl: './connectionlist.component.html',
  styleUrls: ['./connectionlist.component.css']
})
export class ConnectionlistComponent implements OnInit {

  connectionRecords: IConnectionRecords;
  datarecords: Array<IConnectors>;
  rowSelected = false;
  selectedConnRecord: IConnectorDetails = {
    conn_id: -1, conn_system_type: '',
    conn_type: '', name: '',
    conn_logo: '', create_date: '', modified_date: '',
    query_type: 'update',

    sfauth: {
      auth_username: '', auth_password: '',
      auth_host: '', oauth_object_id: '', security_token: ''
    },
    s3auth: {
      aws_access_key_id: '',
      aws_secret_access_key: '', bucket_name: '', aws_region: ''
    }
  }

  @Input()
  filter: string = 'all';

  @Input()
  gridcomp: boolean = true;

  @Input()
  shownew: boolean = true;

  @Output('connection')
  connection: EventEmitter<IConnectorDetails> = new EventEmitter<IConnectorDetails>();

  dataloaded = false;
  errorMessage: string;

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _loadingService: TdLoadingService,
    private router: Router,
    private connectionsService: ConnectionsService,
    private sidSnackbarComponent: SidSnackbarComponent
  ) {
    this.getConnections();

  }

  ngOnInit(): void {
    this.getConnections();

  }

  getConnections() {
    this._loadingService.register('loadingsid');

    this.connectionsService.getConnections().subscribe(
      result => {
        this.connectionRecords = result;
        // we have to filter the records
        this.filterRecords();
        this._loadingService.resolve('loadingsid')

        this.dataloaded = true;
        this._changeDetectorRef.detectChanges();

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsid');
        this.sidSnackbarComponent.systemError();

      })

  }

  filterRecords() {
    // angular does not detect changes in the array
    // so best to load this temporary
    let newdatarecords = this.connectionRecords.records.connectors;
    if (this.filter == 'input') {
      newdatarecords = this.connectionRecords.records.connectors.filter(
        (obj => obj.conn_type === 'AWS_S3' || obj.conn_type === 'File' || obj.conn_type == 'Salesforce')
      );
    }
    else if (this.filter == 'output') {
      newdatarecords = this.connectionRecords.records.connectors.filter(
        (obj => obj.conn_type === 'AWS_S3' || obj.conn_type === 'File' || obj.conn_type == 'Salesforce')
        // (obj => obj.conn_type == 'Salesforce')
      );
    }
    else if(this.filter == 'AWS_S3'){
      newdatarecords = this.connectionRecords.records.connectors.filter(
        (obj => obj.conn_type === 'AWS_S3')
      );
    }
    else if(this.filter == 'Salesforce'){
      newdatarecords = this.connectionRecords.records.connectors.filter(
        (obj => obj.conn_type === 'Salesforce')
      );
    }

    // this.datarecords = newdatarecords;
    this.datarecords = Object.assign([], newdatarecords);


  }

  editConn(conn: IConnectors) {
    this.populateComp(conn);
    this.connection.emit(this.selectedConnRecord)
  }


  populateComp(conn: IConnectors) {
    // populate sf details

    this.selectedConnRecord.conn_id = conn.id;
    this.selectedConnRecord.conn_system_type = conn.conn_system_type;
    this.selectedConnRecord.conn_type = conn.conn_type;
    this.selectedConnRecord.name = conn.name;
    this.selectedConnRecord.conn_logo = conn.conn_logo;
    this.selectedConnRecord.query_type = 'update';
    // now we find corresponding auth details

    let auth_rec;
    auth_rec = this.searchAuth(conn.id, conn.name, conn.conn_type);

    if (!auth_rec) {
      // error
      if(conn.conn_type != 'File'){
        this.sidSnackbarComponent.showMessage('Error: Auth record not found');

      }
      return
    }
    if (conn.conn_type == 'Salesforce') {
      this.selectedConnRecord.sfauth.auth_host = auth_rec.auth_host;
      this.selectedConnRecord.sfauth.auth_password = auth_rec.auth_password;
      this.selectedConnRecord.sfauth.auth_username = auth_rec.auth_username;
      this.selectedConnRecord.sfauth.security_token = auth_rec.security_token;

    }
    else if (conn.conn_type == 'AWS_S3') {
      this.selectedConnRecord.s3auth.aws_access_key_id = auth_rec.aws_access_key_id;
      this.selectedConnRecord.s3auth.aws_secret_access_key = auth_rec.aws_secret_access_key;
      this.selectedConnRecord.s3auth.bucket_name = auth_rec.bucket_name;
      this.selectedConnRecord.s3auth.aws_region = auth_rec.aws_region;
    }

  }

  searchAuth(conn_id, conn_name, conn_type) {
    // find appropriate Auth details for connector
    let searchDataset = [];
    if (this.connectionRecords.status == 'ok') {

      if (conn_type == 'Salesforce') {
        searchDataset = this.connectionRecords.records.sfauth;
      }
      else if (conn_type == 'AWS_S3') {
        searchDataset = this.connectionRecords.records.s3auth;
      }

    }
    if (!searchDataset || searchDataset.length < 1) {
      return null
    }
    let objIndex = searchDataset.findIndex(
      (obj => obj.id === conn_id && obj.name == conn_name));
    if (objIndex > -1) {
      return searchDataset[objIndex]
    }
    return null
  }


  newConn() {
    this.router.navigate(['newconnection']);
  }

  filterConnector(displayName: string = '') {

    this.datarecords = this.connectionRecords.records.connectors.filter(
      (obj) => {
        return obj.name.toLowerCase().indexOf(displayName.toLocaleLowerCase()) > -1;
      });


  }

}
