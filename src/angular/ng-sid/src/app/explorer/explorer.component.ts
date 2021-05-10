import { Component, OnInit } from '@angular/core';
import { IConnectorDetails } from '../models/connection';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.css']
})
export class ExplorerComponent implements OnInit {

  rowSelected = false;
  selectedConnRecord: IConnectorDetails;
  shownew: boolean = false;

  constructor(
    private sidSnackbarComponent: SidSnackbarComponent
  ) {
  }

  ngOnInit(): void {
  }

  selectedConnection(event) {

    this.selectedConnRecord = event;
    if (this.selectedConnRecord.conn_type != 'AWS_S3'){
      this.sidSnackbarComponent.showMessage('Connector not Supported for explorer');

    }
    else{
      this.rowSelected = true;
    }
  }

  backConn() {
    this.rowSelected = false;
  }



}
