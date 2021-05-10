import { Component, OnInit } from '@angular/core';

import { Router, ActivatedRoute } from '@angular/router';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms'; // new add
import { FormControl } from '@angular/forms';

import { ITdDataTableColumn } from '@covalent/core/data-table';


import { TdLoadingService } from '@covalent/core/loading';

import { ConnectionsService } from '../../services/connections.service';
import { IDimRecords, IDimConnectors } from '../../models/dimensions';
import { ISFConnector } from '../../models/salesforce';
import { IS3Connector } from '../../models/awss3';
import { DimensionDataService } from '../../data/dimensiondata.service';

import { SalesforceComponent } from '../salesforce/salesforce.component';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'app-newconnection',
  templateUrl: './newconnection.component.html',
  styleUrls: ['./newconnection.component.css']
})
export class NewconnectionComponent implements OnInit {
  // dimconnectionRecords: IDimRecords;
  dimConnections: Array<IDimConnectors>;
  dataloaded = false;
  allowForm = false;
  errorMessage: string;
  selectedConn: IDimConnectors;
  sfInputRecord: ISFConnector;
  s3InputRecord: IS3Connector;

  constructor(
    private _loadingService: TdLoadingService,
    private router: Router,
    private connectionsService: ConnectionsService,
    private dimensionDataService: DimensionDataService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {

    this.getConnections();
  }

  ngOnInit(): void {
  }

  getConnections() {
    this._loadingService.register('loadingsidconn');

    this.dimensionDataService.dimensionRecord.subscribe(
      result => {
        this._loadingService.resolve('loadingsidconn');
        if (result.records) {
          this.dimConnections = result.records.dimconnectors;
          this.dataloaded = true;

        }

      }
    )


  }

  connSelected(conn: IDimConnectors) {
    this.selectedConn = conn;

    if (conn.conn_name == 'Salesforce' || conn.conn_name == 'AWS_S3') {
      this.allowForm = true;
      // this.errorMessage = 'Connector is work in progress and not allowed at this stage';
    }
    else {
      this.allowForm = false;
      this.sidSnackbarComponent.showMessage('Connector is disabled');

    }
  }

  searchConn() {
    this.router.navigate(['connections']);
  }

}
