import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { TdLoadingService } from '@covalent/core/loading';

import { ConnectionsService } from '../../services/connections.service';
import { IConnectionRecords, IConnectors, IConnectorDetails } from '../../models/connection';
import { IDimConnectors } from '../../models/dimensions';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'app-searchconnections',
  templateUrl: './searchconnections.component.html',
  styleUrls: ['./searchconnections.component.css']
})
export class SearchConnectionsComponent implements OnInit {

  rowSelected = false;
  selectedConnRecord: IConnectorDetails;
  shownew: boolean = true;


  constructor(
    private _loadingService: TdLoadingService,
    private sidSnackbarComponent: SidSnackbarComponent
    ) {
  }

  ngOnInit(): void {
  }


  selectedConnection(event) {
    this.editConn(event);
  }

  editConn(conn: IConnectorDetails) {
    this.selectedConnRecord = conn;
    this.rowSelected = true;
  }

  backConn() {
    this.rowSelected = false;
  }

  closeRecord(event){
    this.rowSelected = false;
  }


}
