import { Component, OnInit } from '@angular/core';

import { HttpErrorResponse } from '@angular/common/http';

import { Router, ActivatedRoute } from '@angular/router';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms'; // new add
import { FormControl } from '@angular/forms';

import { ITdDataTableColumn } from '@covalent/core/data-table';
import { TdDataTableService, TdDataTableSortingOrder, ITdDataTableSortChangeEvent, } from "@covalent/core/data-table";
import { IPageChangeEvent } from '@covalent/core/paging';

import { TdLoadingService } from '@covalent/core/loading';

import { JoblogsService } from '../services/joblogs.service';
import { IJoblogsRecords, Ijoblogs, IJoblogRec } from '../models/joblogs';
import * as moment from 'moment';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'app-joblogs',
  templateUrl: './joblogs.component.html',
  styleUrls: ['./joblogs.component.css']
})
export class JoblogsComponent implements OnInit {

  jobRecords: IJoblogsRecords;
  selectedRec: IJoblogRec;

  configWidthColumns: ITdDataTableColumn[] = [
    { name: 'jobrun_id', label: 'Log id', width: 100 },
    { name: 'job_name', label: 'Job name', width: 250 },
    { name: 'run_type', label: 'Type', width: { min: 20, max: 50 } },
    { name: 'run_date', label: 'Run Date', width: 150 },
    { name: 'status', label: 'Job Status', width: 150 },
    { name: 'total_count', label: 'Record Count', width: 100 },
    { name: 'filename', label: 'filename' },

  ];

  minDate = new Date(2020, 1, 1);
  maxDate = new FormControl(new Date());

  sDate = (new Date()).setDate((new Date()).getDate() - 30);
  selectStartDate = new FormControl(new Date(), Validators.required);
  selectEndDate = new FormControl(new Date(), Validators.required);
  downloadfile = false;

  filteredData: any[] = [];
  filteredTotal = 0;
  rowSelected = false;
  searchTerm = "";
  fromRow = 1;
  currentPage = 1;
  pageSize = 50;
  sortBy = "jobrun_id";
  selectedRow: any[] = [];
  sortOrder: TdDataTableSortingOrder = TdDataTableSortingOrder.Descending;

  dataloaded = false;
  allowForm = false;
  errorMessage: string;

  constructor(
    private _loadingService: TdLoadingService,
    private router: Router,
    private _dataTableService: TdDataTableService,
    private joblogsService: JoblogsService,
    private sidSnackbarComponent: SidSnackbarComponent
  ) {

    let now = new Date();
    let monthAgo = new Date();
    monthAgo.setMonth(now.getMonth() - 1);
    this.selectStartDate = new FormControl(monthAgo, Validators.required);
    // this.selectStartDate.setValue(this.sDate.toISOString());
    // console.log(this.selectStartDate);
    this.getJobs();
  }

  ngOnInit(): void {
  }

  getJobs() {
    this._loadingService.register('loadingsid');
    let startDate = moment(this.selectStartDate.value);
    let endDate = moment(this.selectEndDate.value);

    this.joblogsService.getLogs(
      String(startDate.valueOf()), String(endDate.valueOf())
    ).subscribe(
      result => {
        //  console.log(result);
        this._loadingService.resolve('loadingsid')
        this.jobRecords = result;
        this.filterTable();
        this.dataloaded = true;
      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsid');
        this.sidSnackbarComponent.systemError();

      })
  }
  search(searchTerm: string): void {
    this.searchTerm = searchTerm;
    this.filterTable();
  }
  page(pagingEvent: IPageChangeEvent): void {
    this.fromRow = pagingEvent.fromRow;
    this.currentPage = pagingEvent.page;
    this.pageSize = pagingEvent.pageSize;
    this.filterTable();
  }

  showAlert(event: any): void {
    const row: any = event.row;
    // .. do something with event.row
  }

  filterTable() {
    let newData = this.jobRecords.records.joblogs;
    if (Object.keys(newData).length === 0 && newData.constructor === Object) {
      return;
    }
    const excludedColumns: string[] = this.configWidthColumns
      .filter((column: ITdDataTableColumn) => {
        return (
          (column.filter === undefined && column.hidden === true) ||
          (column.filter !== undefined && column.filter === false)
        );
      })
      .map((column: ITdDataTableColumn) => {
        return column.name;
      });

    newData = this._dataTableService.filterData(
      newData,
      this.searchTerm,
      true,
      excludedColumns
    );

    newData = this._dataTableService.filterData(
      newData, this.searchTerm, true, excludedColumns);
    this.filteredTotal = newData.length;
    newData = this._dataTableService.sortData(
      newData, this.sortBy, this.sortOrder);
    newData = this._dataTableService.pageData(
      newData, this.fromRow, this.currentPage * this.pageSize);
    this.filteredData = newData;

  }

  selectRecord(event: any) {

    this.selectedRec = this.jobRecords.records.joblogs.filter(
      data => {
        return data.jobrun_id == event.row.jobrun_id;
      }
    )[0];
    this.router.navigate(['/joblogdetails', event.row.jobrun_id]);
    this.rowSelected = true;
  }

  onSubmit(): void {
    let startDate = moment(this.selectStartDate.value);
    let endDate = moment(this.selectEndDate.value);
    if (!startDate.isValid() || !endDate.isValid()) {
      this.sidSnackbarComponent.showMessage('Invalid Date');

    }
    this.getJobs();

  }

  cancelLog() {
    this.rowSelected = false;
  }

}
