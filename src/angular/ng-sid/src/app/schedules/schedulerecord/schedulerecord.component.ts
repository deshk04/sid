import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FormControl } from '@angular/forms';

import { ITdDataTableColumn } from '@covalent/core/data-table';
import { TdDataTableService, TdDataTableSortingOrder, ITdDataTableSortChangeEvent, } from "@covalent/core/data-table";
import { IPageChangeEvent } from '@covalent/core/paging';

import { Router, ActivatedRoute } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';

import { SchedulesService } from '../../services/schedules.service';
import { IScheduleSelect, ISchedule, ISchedulelog, IScheduleJobrun } from '../../models/schedule';
import * as moment from 'moment';

import { JoblogsService } from '../../services/joblogs.service';
import { saveAs as importedSaveAs } from 'file-saver';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'schedulerecord',
  templateUrl: './schedulerecord.component.html',
  styleUrls: ['./schedulerecord.component.css']
})

export class SchedulerecordComponent implements OnInit {

  markasComplete = false;
  schRunDate = new FormControl(new Date(), Validators.required);
  schedule_id: number;

  scheduleRecord: IScheduleSelect;

  // @Output('close')
  // closeflag: EventEmitter<boolean> = new EventEmitter<boolean>();


  dataloaded = false;
  logloaded = false;
  logSelected = false;
  scheduleLogRecord: Array<ISchedulelog>;
  groupedRecords;

  configWidthColumns: ITdDataTableColumn[] = [
    { name: 'schedulelog_id', label: 'Id', width: 30 },
    { name: 'run_date', label: 'Run Date', width: 150 },
    { name: 'status', label: 'Status', width: 100 },
    { name: 'start_date', label: 'Start Time', width: 200 },
    { name: 'end_date', label: 'End Time', width: 200 },
    { name: 'message', label: 'message', width: 390 },

  ];

  filteredData: any[] = [];
  filteredTotal = 0;
  selectedRec: ISchedulelog;
  rowSelected = false;
  searchTerm = "";
  fromRow = 1;
  currentPage = 1;
  pageSize = 50;
  sortBy = "schedulelog_id";
  selectedRow: any[] = [];
  sortOrder: TdDataTableSortingOrder = TdDataTableSortingOrder.Descending;
  minDate = new Date(2020, 1, 1);
  maxDate = new FormControl(new Date());

  currDate = new Date();
  sDate = (new Date()).setDate((new Date()).getDate() - 30);
  selectStartDate = new FormControl(new Date(), Validators.required);
  selectEndDate = new FormControl(new Date(), Validators.required);


  constructor(
    private _loadingService: TdLoadingService,
    private schedulesService: SchedulesService,
    private _dataTableService: TdDataTableService,
    private joblogsService: JoblogsService,
    private router: Router,
    private route: ActivatedRoute,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {

    let now = new Date();
    let monthAgo = new Date();
    monthAgo.setMonth(now.getMonth() - 1);
    this.selectStartDate = new FormControl(monthAgo, Validators.required);
    this.schedule_id = this.route.snapshot.params['id'];
    this.getSchedule();

  }

  ngOnInit(): void {
    // console.log(this.groupedRecords);

  }

  getSchedule() {
    this._loadingService.register('loadingsidsch');

    this.schedulesService.getScheduleById(
      String(this.schedule_id)).subscribe(
      result => {
        this._loadingService.resolve('loadingsidsch')
        if(result.status != 'ok'){
          this.sidSnackbarComponent.showMessage(result.message);
          return
        }
        this.scheduleRecord = result.records;
        this.getScheduleLog();
        this.dataloaded = true;
        this.groupedRecords = this.groupByKey(this.scheduleRecord.scheduleconfig, 'job_sequence');
      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsidsch');
        this.sidSnackbarComponent.systemError();

      })
  }


  editSchedule(sch: ISchedule) {

    // we have to send the selected record to output
    // this.update.emit(this.selectedSchConfigs)
  }

  groupByKey(array, key) {
    return array
      .reduce((hash, obj) => {
        if (obj[key] === undefined) return hash;
        return Object.assign(hash, { [obj[key]]: (hash[obj[key]] || []).concat(obj) })
      }, {});
  }

  runschedule() {

    const runDate = moment(this.schRunDate.value);
    let markComplete = 'N';
    if (!runDate.isValid()) {
      this.sidSnackbarComponent.showMessage('Invalid Date');
      return;
    }
    if (this.markasComplete) {
      markComplete = 'Y'
    }
    this._loadingService.register('loadingsidsch');

    this.schedulesService.runSchedule(
      String(this.scheduleRecord.schedules.id),
      String(runDate.valueOf()), markComplete
    ).subscribe(
      result => {
        this._loadingService.resolve('loadingsidsch')
        this.sidSnackbarComponent.showMessage(result.message);

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsidsch');
        this.sidSnackbarComponent.systemError();

      })

  }

  getScheduleLog() {
    this._loadingService.register('loadingsidsch');
    let startDate = moment(this.selectStartDate.value);
    let endDate = moment(this.selectEndDate.value);

    this.schedulesService.getScheduleLog(
      String(this.scheduleRecord.schedules.id),
      String(startDate.valueOf()),
      String(endDate.valueOf())
    ).subscribe(
      result => {
        this._loadingService.resolve('loadingsidsch')
        if(result.status != 'ok'){
          this.sidSnackbarComponent.showMessage(result.message);
          return
        }

        this.scheduleLogRecord = result.records;
        this.filterTable();
        this.logloaded = true;

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsidsch');
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
    let newData = this.scheduleLogRecord;
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

    this.selectedRec = this.scheduleLogRecord.filter(
      data => {
        return data.schedulelog_id == event.row.schedulelog_id;
      }
    )[0];
    this.rowSelected = true;

  }

  redirectLog(jobrun_id){
    this.router.navigate(['/joblogdetails',jobrun_id])
  }
  redirectJob(job_id){
    this.router.navigate(['/jobdetails',job_id])
  }


  downLoadLog(job: IScheduleJobrun) {
    // download the log file
    let downloadfile = false;

    if (job.total_count && job.total_count > 0) {
      if ((job.failure_count && job.failure_count > 0) || (
        job.warning_count && job.warning_count > 0)
      ) {
        downloadfile = true;
      }
    }
    if (!downloadfile) {
      this.sidSnackbarComponent.showMessage('Log file not available');
      return;
    }

    this._loadingService.register("loadingsidsch");
    this.joblogsService.downloadLog(
      String(job.jobrun_id)).subscribe(
        blob => {
          // const date = new Date().toLocaleDateString();
          this.selectedRec.run_date
          const fileName = 'sid_log_'.concat(job.job_name).concat(
            job.run_date).concat('.xlsx');
          importedSaveAs(blob, fileName);
          this._loadingService.resolve("loadingsidsch");
        },
        error => {
          this.sidSnackbarComponent.showMessage('Download Error');
          this._loadingService.resolve("loadingsidsch");
        }
      );
  }
  cancelLog(){
    this.rowSelected = false;
  }
  updateSchedule() {
    this.router.navigate(['/editschedule', this.schedule_id, 'e']);
  }
  cloneSchedule(){
    this.router.navigate(['/editschedule', this.schedule_id, 'c']);
  }

  deleteSchedule(){

  }

}
