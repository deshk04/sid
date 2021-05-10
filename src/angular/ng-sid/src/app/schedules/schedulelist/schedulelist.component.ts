import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { Router } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';

import { SchedulesService } from '../../services/schedules.service';
import { IScheduleRecords, ISchedule, IScheduleConfig, IScheduleSelect, initScheduleRecord } from '../../models/schedule';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'schedulelist',
  templateUrl: './schedulelist.component.html',
  styleUrls: ['./schedulelist.component.css']
})

export class SchedulelistComponent implements OnInit {

  scheduleRecords: IScheduleRecords;
  datarecords: Array<ISchedule>;
  rowSelected = false;
  selectedSchdRecord: IScheduleSelect = JSON.parse(JSON.stringify(initScheduleRecord));

  @Output('select')
  update: EventEmitter<IScheduleSelect> = new EventEmitter<IScheduleSelect>();

  dataloaded = false;

  constructor(
    private _loadingService: TdLoadingService,
    private router: Router,
    private schedulesService: SchedulesService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {

    this.getSchedules();
  }

  ngOnInit(): void {
  }

  getSchedules() {
    this._loadingService.register('loadingsidsched');

    this.schedulesService.getSchedules().subscribe(
      result => {
        this._loadingService.resolve('loadingsidsched')
        this.scheduleRecords = result;
        this.datarecords = this.scheduleRecords.records.schedules;
        this.dataloaded = true;
      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsidsched');
        this.sidSnackbarComponent.systemError();

      })
  }

  newSchedule() {
    //this.sidSnackbarComponent.showMessage('Functionality not available');
    this.router.navigate(['/editschedule', -1, 'e']);
  }

  editSchedule(sch: ISchedule) {
    // this.selectedSchdRecord = sch;
    this.selectedSchdRecord.schedules = sch;
    this.selectedSchdRecord.scheduleconfig = this.searchSchedule(sch.id);

    // this.selectedSchConfigs = this.searchSchedule(sch.id)

    // we have to send the selected record to output
    this.update.emit(this.selectedSchdRecord);
  }
  backSchedule() {
    this.rowSelected = false;
  }
  updateSchedule() {
    // disabled for now
  }

  groupByKey(array, key) {
    return array
      .reduce((hash, obj) => {
        if (obj[key] === undefined){ return hash; }
        return Object.assign(hash, { [obj[key]]: (hash[obj[key]] || []).concat(obj) })
      }, {});
  }

  searchSchedule(schedule_id) {
    // find appropriate Auth details for connector
    let outputRecs: Array<IScheduleConfig>;
    let searchDataset = [];
    if (this.scheduleRecords.status === 'ok') {
      searchDataset = this.scheduleRecords.records.scheduleconfig;
    }
    if (!searchDataset || searchDataset.length < 1) {
      return outputRecs;
    }
    outputRecs = searchDataset.filter(
      (obj => obj.id === schedule_id));
//    console.log(this.groupByKey(outputRecs, 'job_sequence'));
    return outputRecs;

  }




}
