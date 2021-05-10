import { Component, OnInit } from '@angular/core';

import { HttpErrorResponse } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';

import { TdLoadingService } from '@covalent/core/loading';

import { JoblogsService } from '../../services/joblogs.service';
import { IJoblogsRecords, Ijoblogs, IJoblogRec } from '../../models/joblogs';
import {saveAs as importedSaveAs} from 'file-saver';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';


@Component({
  selector: 'app-joblogdetails',
  templateUrl: './joblogdetails.component.html',
  styleUrls: ['./joblogdetails.component.css']
})
export class JoblogdetailsComponent implements OnInit {
  selectedRec: IJoblogRec;
  dataloaded = false;
  jobrun_id: number;
  downloadfile = false;

  constructor(
    private _loadingService: TdLoadingService,
    private route: ActivatedRoute,
    private joblogsService: JoblogsService,
    private sidSnackbarComponent: SidSnackbarComponent
  ) {
    this.jobrun_id = this.route.snapshot.params['id'];

    this.getJobLog();

  }

  ngOnInit(): void {
  }

  getJobLog(){
    this._loadingService.register('loadingsid');

    this.joblogsService.getLogById(
      String(this.jobrun_id)
    ).subscribe(
      result => {
        this._loadingService.resolve('loadingsid')
        if(result.status != 'ok' || result.records.joblogs.length < 1) {
          this.sidSnackbarComponent.showMessage('Error fetching log details');
          return
        }
        this.selectedRec = result.records.joblogs[0];
        this.dataloaded = true;

        this.downloadfile = false;

        if (this.selectedRec.total_count && this.selectedRec.total_count > 0) {
          if ((this.selectedRec.failure_count && this.selectedRec.failure_count > 0) || (
            this.selectedRec.warning_count && this.selectedRec.warning_count > 0)
          ) {
            this.downloadfile = true;
          }
        }
        if (!this.downloadfile) {
          this.sidSnackbarComponent.showMessage('Log file not available: No failed records', true);
          //return;
        }


      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsid');
        this.sidSnackbarComponent.systemError();

      })

  }

  downLoadLog() {
    // download the log file

    this._loadingService.register("loadingsid");
    this.joblogsService.downloadLog(
      String(this.selectedRec.jobrun_id)).subscribe(
      blob => {
        // const date = new Date().toLocaleDateString();
        this.selectedRec.run_date
        const fileName = 'sid_log_'.concat(this.selectedRec.job_name).concat(
          this.selectedRec.run_date).concat('.xlsx');
        importedSaveAs(blob, fileName);
        this._loadingService.resolve("loadingsid");
      },
      error => {
        this._loadingService.resolve("loadingsid");
        this.sidSnackbarComponent.showMessage('Download Error');

      }
    );

  }

  runfailedRecs() {
    // download the log file

    this._loadingService.register("loadingsid");
    this.joblogsService.runJobByJobRunId(
      String(this.selectedRec.job_id),
      String(this.selectedRec.jobrun_id)).subscribe(
        result => {
          if(result.status == 'ok'){
            this.sidSnackbarComponent.showMessage(result.message, true);
          }
          else{
            this.sidSnackbarComponent.showMessage(result.message);
          }
        this._loadingService.resolve("loadingsid");
      },
      error => {
        this._loadingService.resolve("loadingsid");
        this.sidSnackbarComponent.showMessage('Download Error');
      }
    );

  }



}
