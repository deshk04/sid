import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import {SnotifyService, SnotifyPosition} from 'ng-snotify';

@Component({
  selector: 'app-sidsnackbar',
  templateUrl: './sidsnackbar.component.html',
  styleUrls: ['./sidsnackbar.component.css']
})
export class SidSnackbarComponent implements OnInit {

  timeOut = 1500;
  msgConfig = new MatSnackBarConfig();
  snotifyConfig = {
    timeout: 2000,
    showProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    position: SnotifyPosition.rightTop,
    bodyMaxLength: 1000,

  };

  snotifyErrorConfig = {
    timeout: 0,
    showProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    position: SnotifyPosition.rightTop,
    bodyMaxLength: 1000,

  };

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    public _matSnackBar: MatSnackBar,
    private snotifyService: SnotifyService
    ) {
      this.msgConfig.panelClass = ["sid-snackbar"];
      this.msgConfig.duration = 6000;
      this.msgConfig.verticalPosition = 'top';
      this.msgConfig.horizontalPosition = 'right';
    }

  ngOnInit(): void {
  }

  showSnackMessage(message) {

    if ( message instanceof Array) {
      message.forEach( (msg, index) => {
        setTimeout(() => {
            this._matSnackBar.open(msg, 'Dismiss', this.msgConfig);
        }, index * (this.timeOut+500));
    });

    } else {
      this._matSnackBar.open(message, 'Dismiss', this.msgConfig);
    }
  }

  showMessage(message, success = false) {

    if ( message instanceof Array) {
      message.forEach( (msg) => {
        if(success){
          this.snotifyService.success(msg, this.snotifyConfig);
        }
        else {
          this.snotifyService.error(msg, this.snotifyErrorConfig);
        }
      });

    } else {
      if(success){
        this.snotifyService.success(message, this.snotifyConfig);
      }
      else{
        this.snotifyService.error(message, this.snotifyErrorConfig);
      }

    }
    this._changeDetectorRef.detectChanges();
  }
  systemError() {
    this.snotifyService.error('System Error: please check console', this.snotifyErrorConfig);
    this._changeDetectorRef.detectChanges();
  }

  parseResult(result){
    if(result.status == 'ok'){
      this.showMessage(result.message, true);
    }
    else{
      this.showMessage(result.message);
    }
  }

}
