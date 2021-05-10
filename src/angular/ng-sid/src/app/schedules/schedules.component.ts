import { Component, OnInit } from '@angular/core';
import { IScheduleRecords, IScheduleSelect, IScheduleConfig } from '../models/schedule';
import { Router } from '@angular/router';

@Component({
  selector: 'app-schedule',
  templateUrl: './schedules.component.html',
  styleUrls: ['./schedules.component.css']
})
export class SchedulesComponent implements OnInit {

  rowSelected = false;
  selectedScheduleRecord: IScheduleSelect;

  constructor(
    private router: Router
  ) {
  }

  ngOnInit(): void {
  }

  selectedSchedule(event){
    // this.selectedScheduleRecord = event;
    this.router.navigate(['/scheduledetails', event.schedules.id])
  }

  closeRecord(event){
    this.rowSelected = false;
  }


}
