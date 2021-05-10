import { Component, OnInit } from '@angular/core';
import { IConnectorDetails } from '../models/connection';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { ISFParsedQuery } from '../models/salesforce';

@Component({
  selector: 'app-query',
  templateUrl: './query.component.html',
  styleUrls: ['./query.component.css']
})
export class QueryComponent implements OnInit {

  rowSelected = false;
  selectedConnRecord: IConnectorDetails;
  shownew: boolean = false;
  sfjob: ISFParsedQuery = {
    fields: [],
    models: [],
    model_name: '',
    query: {
      query: '', metadata: ''
    },
    connector: {
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

    },
    filter: '',
    download: ''
  }


  constructor(
    private sidSnackbarComponent: SidSnackbarComponent
  ) {
  }

  ngOnInit(): void {
  }

  selectedConnection(event) {

    this.selectedConnRecord = event;
    if (this.selectedConnRecord.conn_type != 'Salesforce'){
      this.sidSnackbarComponent.showMessage('Connector not Supported for query');
    }
    else{
      this.sfjob.connector = this.selectedConnRecord;
      this.rowSelected = true;
    }
  }

  SfQuery(event) {
    console.log('Inside...sfQuery');
    console.log(event);
  }

  backConn() {
    this.rowSelected = false;
  }



}
