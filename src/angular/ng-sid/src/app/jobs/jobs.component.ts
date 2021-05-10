import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { IJob } from '../models/jobs';

@Component({
  selector: 'app-jobs',
  templateUrl: './jobs.component.html',
  styleUrls: ['./jobs.component.css'],
})
export class JobsComponent implements OnInit {

  // seletedJobRecord details
  selectedJobRecord: IJob;

  newJobFlag = false;
  // joblist flags
  shownew = false;
  gridshow = true;
  dataloadedflag = false;

  constructor(
    private router: Router
    ) {

  }

  ngOnInit(): void { }


  selectedJob(event: IJob) {
    if(event.job_id < 1) {
      this.router.navigate(['/editjob', 0, 'n']);

    }
    else{
      this.router.navigate(['/jobdetails', event.job_id]);

    }

  }


}
