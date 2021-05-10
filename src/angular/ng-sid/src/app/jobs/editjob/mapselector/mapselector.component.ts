import { Component, EventEmitter, Input, OnChanges, Output, ChangeDetectorRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FormControl } from '@angular/forms';
import { SimpleChanges } from '@angular/core';

import { ITdDataTableColumn } from '@covalent/core/data-table';
import {
  TdDataTableService,
  TdDataTableSortingOrder,
  ITdDataTableSortChangeEvent,
} from '@covalent/core/data-table';
import { IPageChangeEvent } from '@covalent/core/paging';

import { TdLoadingService } from '@covalent/core/loading';
import { IConnectorDetails } from '../../../models/connection';
import { DimensionDataService } from '../../../data/dimensiondata.service';
import { JobsService } from '../../../services/jobs.service';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { IDimMapType, IDimFileMask } from '../../../models/dimensions';

import {
  IJob,
  IJobModels,
  IJobmap,
  IJobFields,
  IJobconfig,
} from '../../../models/jobs';


@Component({
  selector: 'mapselector',
  templateUrl: './mapselector.component.html',
  styleUrls: ['./mapselector.component.css']
})
export class MapselectorComponent implements OnChanges {

  // selectedMapRecord: FormGroup;
  showSelectedMapRecord: boolean = false;
  selectedMapRecord: FormGroup;

  // Datatable related variables
  configWidthColumns: ITdDataTableColumn[] = [
    { name: 'index', label: '#No', width: 50 },
    { name: 'source_field', label: 'Source Field', width: 250 },
    { name: 'map_type', label: 'Map Type', width: 80 },
    { name: 'map_value', label: 'Map Value', width: 100 },
    { name: 'lookup_model', label: 'Lookup Model', width: 100 },
    { name: 'lookup_join_field', label: 'Lookup Join Field', width: 150 },
    { name: 'lookup_return_field', label: 'Return Field', width: 80 },
    { name: 'dest_model', label: 'Dest Model' },
    { name: 'dest_field', label: 'Dest Field' },
  ];
  filteredData: any[] = [];
  filteredTotal = 0;
  searchTerm = '';
  fromRow = 1;
  currentPage = 1;
  pageSize = 50;
  sortBy = 'index';
  selectedRow: any[] = [];
  sortOrder: TdDataTableSortingOrder = TdDataTableSortingOrder.Descending;

  sourceFieldDisable: boolean = true;

  newJobFlag = false;
  cloneJobFlag = false;
  changeSrcConnector = false;
  changeDstConnector = false;
  showSourceQuery = false;

  dimMapTypes: IDimMapType[];
  jobModels: IJobModels[];
  jobDestModelFields: IJobFields[];
  lookupFields: IJobFields[];

  @Input()
  job: IJob;

  @Output()
  ostatus: EventEmitter<boolean> = new EventEmitter<boolean>();

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _formBuilder: FormBuilder,
    private _loadingService: TdLoadingService,
    private _dataTableService: TdDataTableService,
    private jobsService: JobsService,
    private dimensionDataService: DimensionDataService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {
    this.getDimensions();

  }

  // ngOnInit(): void {
  //   this.selectedMapRecord = this.mapForm();
  //   if(this.job.job_id < 0){
  //     this.job.map = [];
  //   }
  //   this.modelMap();

  // }
  ngOnChanges(changes: SimpleChanges){

    for (const propName in changes) {
      if (changes.hasOwnProperty(propName)) {
        switch (propName) {
          case 'job': {
            this.job = changes['job'].currentValue;
          }
        }
      }
    }

    this.selectedMapRecord = this.mapForm();
    if(this.job.job_id < 0){
      this.job.map = [];
    }
    // console.log(this.job);

    this.modelMap();

  }
  getDimensions() {
    this._loadingService.register('loadingsidmapjob');
    this.dimensionDataService.dimensionRecord.subscribe((result) => {
      this._loadingService.resolve('loadingsidmapjob');
      if (result.records) {
        this.dimMapTypes = result.records.dimmaptype;
      }
    });
  }
  mapForm() {
    return this._formBuilder.group({
      source_model: [{ value: '', disabled: false }, Validators.required],
      source_field: [{ value: '', disabled: false }, Validators.required],
      map_type: [{ value: '', disabled: false }, Validators.required],
      map_value: [{ value: '' }],
      lookup_model: [{ value: '' }],
      lookup_join_field: [{ value: '' }],
      lookup_return_field: [{ value: '' }],
      dest_model: [{ value: '', disabled: false }, Validators.required],
      dest_field: [{ value: '', disabled: false }, Validators.required],
      index: [{ value: '' }],
    });
  }

  sort(sortEvent: ITdDataTableSortChangeEvent): void {
    this.sortOrder =
      this.sortOrder === TdDataTableSortingOrder.Ascending
        ? TdDataTableSortingOrder.Descending
        : TdDataTableSortingOrder.Ascending;
    this.sortBy = sortEvent.name;
    this.filterTable();
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
  filterTable() {
    let newData = this.job.map;
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
      newData,
      this.searchTerm,
      true,
      excludedColumns
    );
    this.filteredTotal = newData.length;
    newData = this._dataTableService.sortData(
      newData,
      this.sortBy,
      this.sortOrder
    );
    newData = this._dataTableService.pageData(
      newData,
      this.fromRow,
      this.currentPage * this.pageSize
    );
    this.filteredData = newData;
  }

  /*
    Map datatable related function
  */
  selectMapRecord(event: any) {

    this.selectedMapRecord.patchValue({
      source_model: event.row.source_model,
      source_field: event.row.source_field,
      map_type: event.row.map_type,
      map_value: event.row.map_value,
      lookup_model: event.row.lookup_model,
      lookup_join_field: event.row.lookup_join_field,
      lookup_return_field: event.row.lookup_return_field,
      dest_model: event.row.dest_model,
      dest_field: event.row.dest_field,
      index: event.row.index,
    });
    if (event.row.lookup_model != null) {
      this.fetchModels(event.row.lookup_model);
    }

    this.showSelectedMapRecord = true;
  }

  updateMap() {
    if (this.validateUpdateMap()) {

      const idx = this.selectedMapRecord.controls['index'].value;

      if (idx >= 0) {

        this.job.map[idx].source_model = this.selectedMapRecord.controls['source_model'].value;
        this.job.map[idx].source_field = this.selectedMapRecord.controls['source_field'].value;
        this.job.map[idx].map_type = this.selectedMapRecord.controls['map_type'].value;
        this.job.map[idx].map_value = this.selectedMapRecord.controls['map_value'].value;
        this.job.map[idx].lookup_model = this.selectedMapRecord.controls['lookup_model'].value;
        this.job.map[idx].lookup_join_field = this.selectedMapRecord.controls['lookup_join_field'].value;
        this.job.map[idx].lookup_return_field = this.selectedMapRecord.controls['lookup_return_field'].value;
        this.job.map[idx].dest_model = this.selectedMapRecord.controls['dest_model'].value;
        this.job.map[idx].dest_field = this.selectedMapRecord.controls['dest_field'].value;

      }
      else {
        var newMap: IJobmap =
        {
          source_model: this.selectedMapRecord.controls['source_model'].value,
          source_field: this.selectedMapRecord.controls['source_field'].value,
          map_type: this.selectedMapRecord.controls['map_type'].value,
          map_value: this.selectedMapRecord.controls['map_value'].value,
          lookup_model: this.selectedMapRecord.controls['lookup_model'].value,
          lookup_join_field: this.selectedMapRecord.controls['lookup_join_field'].value,
          lookup_return_field: this.selectedMapRecord.controls['lookup_return_field'].value,
          dest_model: this.selectedMapRecord.controls['dest_model'].value,
          dest_field: this.selectedMapRecord.controls['dest_field'].value,
          index: this.job.map.length
        }
        this.job.map.push(newMap);
      }

      this.filterTable();
      this.showSelectedMapRecord = false;
      this.sourceFieldDisable = true;
      this._changeDetectorRef.detectChanges();

    }
  }

  validateUpdateMap() {

    let returnMessages = [];
    this._changeDetectorRef.detectChanges();

    // if (this.selectedMapRecord.controls['source_model'].value == '' ||
    //   this.selectedMapRecord.controls['source_model'].value == null) {
    //   returnMessages.push('Invalid Source Model');
    // }

    // if (this.selectedMapRecord.controls['dest_model'].value == '' ||
    //   this.selectedMapRecord.controls['dest_model'].value == null) {
    //   returnMessages.push('Invalid Dest Model');
    // }

    if (this.selectedMapRecord.controls['source_field'].value == '' ||
      this.selectedMapRecord.controls['source_field'].value == null) {
      returnMessages.push('Invalid Source Field');
    }

    if (this.selectedMapRecord.controls['dest_field'].value == '' ||
      this.selectedMapRecord.controls['dest_field'].value == null) {
      returnMessages.push('Invalid Dest Field');
    }


    if (this.selectedMapRecord.controls['map_type'].value == null ||
      this.selectedMapRecord.controls['map_type'].value == 'map_n_hook') {
      returnMessages.push('Invalid Map Type or not supported');
    }
    else {

      if ((this.selectedMapRecord.controls['map_type'].value == 'lookup')
        && (
          (this.selectedMapRecord.controls['lookup_model'].value == null)
          || (this.selectedMapRecord.controls['lookup_model'].value.length == 0)
          || (this.selectedMapRecord.controls['lookup_join_field'].value == null)
          || (this.selectedMapRecord.controls['lookup_join_field'].value.length == 0)
          || (this.selectedMapRecord.controls['lookup_return_field'].value == null)
          || (this.selectedMapRecord.controls['lookup_return_field'].value.length == 0)
        )) {
        returnMessages.push('Lookup details missing');
      }
      if ((this.selectedMapRecord.controls['map_type'].value == 'constant')
        && (
          (this.selectedMapRecord.controls['map_value'].value == null)
          || (this.selectedMapRecord.controls['map_value'].value == '')
        )) {
        returnMessages.push('Constant details missing');
      }
      if (this.selectedMapRecord.controls['map_type'].value == 'map_n_hook') {
        returnMessages.push('map_n_hook not supported');
      }

    }

    /* check if we found any error */
    if (returnMessages.length > 0) {
      this.sidSnackbarComponent.showMessage(returnMessages);

      return false;
    }
    return true;
  }
  validateMap() {

    let errorMessages = [];
    this._changeDetectorRef.detectChanges();

    this.job.map.forEach(function (element, idx) {
      if (element.map_type == null || element.map_type == '') {
        errorMessages.push('Invalid Map Type: record # '.concat(idx.toString()));
      }
      else {
        if(element.map_type == 'map' &&
        (element.dest_field == null || element.dest_field == '')){
          errorMessages.push('Destination field missing: record # '.concat(idx.toString()));
        }
        else if ((element.map_type == 'lookup') && (
            (element.lookup_model == null)
            || (element.lookup_model.length == 0)
            || (element.lookup_join_field == null)
            || (element.lookup_join_field.length == 0)
            || (element.lookup_return_field == null)
            || (element.lookup_return_field.length == 0)
          )) {
          errorMessages.push('Lookup details missing: record # '.concat(idx.toString()));
        }
        else if ((element.map_type == 'constant')
          && (
            (element.map_value == null)
            || (element.map_value == '')
          )) {
          errorMessages.push('Constant details missing: record # '.concat(idx.toString()));
        }

      }

    });

    /* check if we found any error */
    if (errorMessages.length > 0) {
      this.sidSnackbarComponent.showMessage(errorMessages);
      return false;
    }
    return true;
  }


  cancelMap() {
    this.showSelectedMapRecord = false;
    this.sourceFieldDisable = true;

  }

  deleteMap() {
    this.showSelectedMapRecord = false;
    const idx = this.selectedMapRecord.controls['index'].value;
    this.job.map.splice(idx, 1);
    this.job.map.forEach((element, idx) => {
      element.index = idx;
    });

    this.filterTable();
    this.sourceFieldDisable = true;

  }
  addNewMap() {

    this.setMapRecord();

    this.showSelectedMapRecord = true;
    this.sourceFieldDisable = false;

  }
  setMapRecord() {
    this.selectedMapRecord.patchValue({
      lookup_join_field: '',
      lookup_return_field: '',
      lookup_model: '',
      source_model: this.job.source_config.filestartwith,
      dest_model: this.job.map[0].dest_model,
      map_value: '',
      index: -1
    });


  }
  fetchModels(model_name) {
    this._loadingService.register('loadingsidmapjob');

    this.jobsService
      .fetchConnModels(
        String(this.job.dest_config.conn_id),
        model_name
      )
      .subscribe(
        (result) => {
          this.lookupFields = result.records.fields;
          this._loadingService.resolve('loadingsidmapjob');

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsidmapjob');
          this.sidSnackbarComponent.systemError();

        }
      );


  }

  modelChange(model_name) {
    this.fetchModels(model_name);
    // remove lookup fields
    this.selectedMapRecord.patchValue({
      lookup_join_field: '',
      lookup_return_field: '',
    });

  }

  mapChange(map_type){
    if(this.job.dest_config.conn_type != 'Salesforce'){
      this.sidSnackbarComponent.showMessage('Lookup is not available for this connector');
    }
  }

  mapFields(){
    this.job.map = [];
    this.job.sourcefields.forEach((element, idx) => {
      //match it against the destination field
      // element.field_name

      let objIndex = this.job.destfields.findIndex(
        (obj) =>
          obj.field_name.toLowerCase() === element.field_name.toLowerCase()
      );

      if (objIndex == -1) {
        // we should do substring match
        objIndex = this.job.destfields.findIndex(
          (obj) =>
            obj.field_name.toLowerCase().substring(
              0, element.field_name.length) === element.field_name.toLowerCase()
        );

      }

      if (objIndex > -1) {
        // found the record
        const mapRecord: IJobmap = {
          source_model: this.job.source_config.filestartwith,
          source_field: element.field_name,
          map_type: 'map',
          map_value: '',
          lookup_model: '',
          lookup_join_field: '',
          lookup_return_field: '',
          dest_model: this.job.dest_config.model ,
          dest_field: this.job.destfields[objIndex].field_name,
          index: idx,
        };
        this.job.map.push(mapRecord);
      } else {
        const mapRecord: IJobmap = {
          source_model: this.job.source_config.filestartwith,
          source_field: element.field_name,
          map_type: 'map',
          map_value: '',
          lookup_model: '',
          lookup_join_field: '',
          lookup_return_field: '',
          dest_model: this.job.dest_config.model,
          dest_field: '',
          index: idx,
        };
        this.job.map.push(mapRecord);
      }
    });
    // console.log(this.job);
    this.filterTable();

  }
  modelMap() {
    if (this.job.map.length == 0) {
      this.mapFields();
    }
    else {
      this.job.map.forEach(function (element, i) {
        element.index = i;
      });
      this.filterTable();

    }

  }

  submitForm() {
    if (this.validateMap()) {
      this.ostatus.emit(true);
    }
  }
  cancel(){
    this.ostatus.emit(false);
  }


}
