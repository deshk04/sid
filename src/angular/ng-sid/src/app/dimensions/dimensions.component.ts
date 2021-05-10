import { Component, OnInit, Output } from '@angular/core';
import { TdMediaService } from '@covalent/core/media';
import { TdLoadingService } from '@covalent/core/loading';

import { DimensionsService } from '../services/dimensions.service';
import { DimensionDataService } from '../data/dimensiondata.service';
import { IDimRecords } from '../models/dimensions'
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 'dimensions',
  templateUrl: './dimensions.component.html',
  styleUrls: ['./dimensions.component.css']
})
export class DimensionsComponent implements OnInit {
  recordsFound = false;

@Output()
dimensionRecords: IDimRecords;

  constructor(
    private _loadingService: TdLoadingService,
    private dimensionsService: DimensionsService,
    private dimensionDataService: DimensionDataService,
    private sidSnackbarComponent: SidSnackbarComponent
    ) {
  }

  ngOnInit(): void {
    this.fetchDimensions();
    this.getDimensions();

  }

  getDimensions() {
    this.dimensionDataService.dimensionRecord.subscribe(
      result => {
        if (result.status === 'ok') {
            this.dimensionRecords = result;
            this.recordsFound = true
          }
      },
      err => {
        console.log(err);
        this.sidSnackbarComponent.systemError();
      }
    );
  }

  fetchDimensions(){
    this._loadingService.register('loadingdimsid');

    this.dimensionsService.getdimConnections().subscribe(
      result => {
        this.dimensionRecords = result;
        this.dimensionDataService.dimensionRecord.next(
            this.dimensionRecords
        )

        this._loadingService.resolve('loadingdimsid')
      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingdimsid');
        this.sidSnackbarComponent.systemError();

      })

}



}
