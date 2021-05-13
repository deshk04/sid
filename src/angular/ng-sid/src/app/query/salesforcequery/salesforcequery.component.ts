import { Component, EventEmitter, Input, OnChanges, Output, ChangeDetectorRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { SimpleChanges } from '@angular/core';

import { Router } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';
import { saveAs } from 'file-saver';

import { ITdDataTableColumn } from '@covalent/core/data-table';
import {
  TdDataTableService,
  TdDataTableSortingOrder,
  ITdDataTableSortChangeEvent,
} from '@covalent/core/data-table';
import { IPageChangeEvent } from '@covalent/core/paging';


import { IConnectorDetails } from '../../models/connection';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { SalesforceService } from '../../services/salesforce.service';
import { JobsService } from '../../services/jobs.service';

import { parseQuery, composeQuery, isQueryValid, formatQuery } from 'soql-parser-js';
import { from } from 'rxjs';
import { IJob, IJobFields, IJobModels , IJobquery } from '../../models/jobs';
import { ISFParsedQuery, initsfjob } from '../../models/salesforce';

@Component({
  selector: 'salesforcequery',
  templateUrl: './salesforcequery.component.html',
  styleUrls: ['./salesforcequery.component.css']
})
export class SalesforcequeryComponent implements OnChanges {
  dataloaded: boolean = false;
  downloadFlag: boolean = false;
  sfdata: any[] = [];
  querydataFlag: boolean = false;

  filteredTotal = 0;
  searchTerm = '';
  fromRow = 1;
  currentPage = 1;
  pageSize = 50;
  filteredData: any[] = [];


  @Input()
  job: ISFParsedQuery = JSON.parse(JSON.stringify(initsfjob));

  @Input()
  showdownload: boolean = true;

  @Output()
  status: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _loadingService: TdLoadingService,
    private router: Router,
    private salesforceService: SalesforceService,
    private _dataTableService: TdDataTableService,
    private jobsService: JobsService,
    private sidSnackbarComponent: SidSnackbarComponent
    ) {
      // this.getDimensions();
  }

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
    if(this.showdownload){
      this.job.filter = 'n';
    }
    if(this.job.query === null) {
      this.job.query = {
        query: '',
        metadata: ''
      }
    }

    this.dataloaded = false;
    this.querydataFlag= false;
    this.fetchSfModels('');
  }

  selectedConnection(connector: IConnectorDetails) {
    this.dataloaded = false;
    this.fetchSfModels('');
    // console.log(this.selectedConnRecord.conn_type)
  }


  search(searchTerm: string): void {
    this.searchTerm = searchTerm;
   this.filterTable();
  }
  page(pagingEvent: IPageChangeEvent): void {
    this.fromRow = pagingEvent.fromRow;
    this.currentPage = pagingEvent.page;
    this.pageSize = pagingEvent.pageSize;
  }
  filterTable() {
    let newData = this.sfdata;
    if (Object.keys(newData).length === 0 && newData.constructor === Object) {
      return;
    }
    const excludedColumns: string[] = [];

    newData = this._dataTableService.filterData(
      newData,
      this.searchTerm,
      true,
      excludedColumns
    );

    newData = this._dataTableService.filterData(
      newData,
      this.searchTerm,
      true,
      excludedColumns
    );
    this.filteredTotal = newData.length;
    // newData = this._dataTableService.sortData(
    //   newData,
    //   this.sortBy,
    //   this.sortOrder
    // );
    newData = this._dataTableService.pageData(
      newData,
      this.fromRow,
      this.currentPage * this.pageSize
    );
    this.filteredData = newData;
  }


  fetchSfModels(model_name){
    this._loadingService.register('loadingsidsfquery');

    this.jobsService
      .fetchConnModels (
        String(this.job.connector.conn_id),
        model_name
      )
      .subscribe(
        (result) => {

          // console.log(result);
          this.job.models = result.records.models;
          this.job.fields = result.records.fields;
          this.constructQuery();
          this.dataloaded = true;
          this._changeDetectorRef.detectChanges();
          this._loadingService.resolve('loadingsidsfquery');

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsidsfquery');
          this.sidSnackbarComponent.systemError();

        }
      );


  }

  genQuery(){
    // console.log(this.sfmodel);
    // this.queryFlag = true;
    this.fetchSfModels(this.job.model_name);
  }

  constructQuery(){

    if(this.job.fields.length > 0){

      this.job.query.query = "SELECT ";
      var elemList = []
      this.job.fields.forEach(element => {
        elemList.push(element.field_name);
      });
      this.job.query.query = this.job.query.query.concat(elemList.join(' ,'));
      this.job.query.query = this.job.query.query.concat(' from ');
      this.job.query.query = this.job.query.query.concat(this.job.model_name);

      if(!isQueryValid(this.job.query.query)){
        this.sidSnackbarComponent.showMessage('Error generating Query');
        return;
      }
      var composeq = composeQuery(parseQuery(this.job.query.query));
      this.job.query.query = formatQuery(composeq);
    }
  }

  pasteEvent(event: ClipboardEvent){
    this.job.query.query = event.clipboardData.getData('Text')
  }

  acceptQuery(){
    if(this.job.query.query.length > 0){
      if(!isQueryValid(this.job.query.query)){
        this.sidSnackbarComponent.showMessage('Invalid Query');
        return;
      }
      let sfparsedquery = parseQuery(this.job.query.query);
      var composeq = composeQuery(sfparsedquery,
      {
        format: true,
        formatOptions: {
          fieldSubqueryParensOnOwnLine: true,
          newLineAfterKeywords: true,
          fieldMaxLineLength: 1 }
      }
      );

      this.job.query.query = formatQuery(composeq);
      this.job.query.metadata = sfparsedquery;

    }
    this.sidSnackbarComponent.showMessage('Query submitted for parsing, please wait...', true);
    this._loadingService.register('loadingsidsfquery');
    this.querydataFlag = false;
    this.salesforceService
      .validateSFQuery (
        this.job
      )
      .subscribe(
        (result) => {
          this._loadingService.resolve('loadingsidsfquery');
          if(result.status != 'ok'){
            this.sidSnackbarComponent.showMessage(result.message);
            // this.job.fields = [];
            // this.job.model_name = '';
            return;
          }
          if(this.downloadFlag){
            // console.log('save file...');
            var blob = new Blob([result.records['filedata']], {type: "text/plain;charset=utf-8"});
            saveAs(blob, result.records['filename']);
          }
          else{
            // this.sidSnackbarComponent.showMessage('Query Parsed successful, Please press Next', true);
            this.job.fields = result.records.fields;
            this.job.model_name = 'sfquery';
            this.sfdata = result.records.records;
            //this.filteredTotal = this.sfdata.length;
            this.filterTable();
            this.querydataFlag = true;

          }
          if(!this.showdownload){
            this.status.emit(true);
          }

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsidsfquery');
          this.sidSnackbarComponent.systemError();

        }
      );
  }

  toggleDownload(event){
//    this.downloadFlag = !this.downloadFlag;
    this.job.download = 'Y';
  }

  submit(){
    // if(this.validate()){
    //   this.ostatus.emit(true);
    // }

  }

}
