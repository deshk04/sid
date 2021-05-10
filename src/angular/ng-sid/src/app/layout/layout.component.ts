import { Component, Inject, HostBinding, AfterViewInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { TdMediaService } from '@covalent/core/media';

import { MatDialog }  from '@angular/material/dialog';
import { MatDialogConfig }  from '@angular/material/dialog';
import { MatDialogRef }  from '@angular/material/dialog';

import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';

import { TdLoadingService } from '@covalent/core/loading';
import { IUserProfile } from '../models/userprofile';
import { UserAuthService } from '../services/auth.service';
import { UserProfileDataService } from '../services/userprofiledata.service';
import { tap, map } from 'rxjs/operators';

import { IDimRecords } from '../models/dimensions'
import { DimensionsService } from '../services/dimensions.service';
import { DimensionDataService } from '../data/dimensiondata.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

const defaultDialogConfig = new MatDialogConfig();

@Component({
    changeDetection: ChangeDetectionStrategy.OnPush,
    selector: 'layout',
    styleUrls: ['./layout.component.scss'],
    templateUrl: './layout.component.html',
})
export class LayoutComponent implements AfterViewInit {


    userProfileStatus = false;
    userProfileRecord: IUserProfile;
    userLoggedStatus = false;
    connFlag = false;
    dimensionRecords: IDimRecords;

    constructor(private _changeDetectorRef: ChangeDetectorRef,
        public media: TdMediaService,
        public dialog: MatDialog,
        private router: Router,
        private _loadingService: TdLoadingService,
        private userAuthService: UserAuthService,
        private userProfileDataService: UserProfileDataService,
        private dimensionsService: DimensionsService,
        private dimensionDataService: DimensionDataService,
        private sidSnackbarComponent: SidSnackbarComponent

    ) {
        this.getDimensions()

        if(this.userAuthService.isLoggedIn()){

            this.userLoggedStatus = true;
            this.userProfileRecord = this.userAuthService.profile;

        }
        else{
            this.userAuthService.refreshToken();
        }
        this.userProfileDataService.profileRecord.subscribe(
            response => {
                this.userProfileRecord = response;
                this.userLoggedStatus = response.isLoggedIn;
            }
        )

        // fetch the dimension records
        // fetch the jobs

        }

        ngAfterViewInit(): void {
            // broadcast to all listener observables when loading the page
            setTimeout(() => { // workaround since MatSidenav has issues redrawing at the beggining
            this.media.broadcast();
            this._changeDetectorRef.detectChanges();
        });

    }

    getDimensions(){
        this._loadingService.register('loadinglayoutsid');

        this.dimensionsService.getdimConnections().subscribe(
          result => {
            this.dimensionRecords = result;
            this.dimensionDataService.dimensionRecord.next(
                this.dimensionRecords
            )

            this._loadingService.resolve('loadinglayoutsid')
          },
          err => {
            console.log(err);
            this._loadingService.resolve('loadinglayoutsid');
            this.sidSnackbarComponent.systemError();

          })

    }

    getJobs() {

    }


}
