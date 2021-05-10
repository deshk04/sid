import { Injectable } from '@angular/core';
import { IDimRecords } from '../models/dimensions';

import { BehaviorSubject } from 'rxjs';

// @Injectable()
@Injectable({
    providedIn: 'root'
  })
export class DimensionDataService {
    tempDimension: IDimRecords = { status: '', num_of_records: 0, message: [], records: null };

    dimensionRecord: BehaviorSubject<IDimRecords> = new BehaviorSubject<IDimRecords>(this.tempDimension);
    constructor() { }

}