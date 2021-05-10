export interface IJobModels {
    name: string;
    label: string;
}

export interface IJobFields {
    model_name: string;
    field_name: string;
    field_type: string;
    field_length: string;
    field_format: string;
    label: string;
    primary_key: string;
}

export interface IJobmap {
    source_model: string;
    source_field: string;
    map_type: string;
    map_value: string;
    lookup_model: string;
    lookup_join_field: string;
    lookup_return_field: string;
    dest_model: string;
    dest_field: string;
    index: number;
}

export interface IJobquery{
    query: string,
    metadata: any
}
export interface IJobconfig {
    job_id: number;
    rec_type: string;
    conn_id: number;
    conn_type: string;
    conn_name: string;
    conn_system_type: string;
    conn_logo_path: string;
    filepath: string;
    filestartwith: string;
    fileendwith: string;
    filemask: string;
    delimiter: string;
    encoding: string;
    lineterminator: string;
    archivepath: string;
    key_field: string;
    bulk_count: number;
    query: IJobquery;
    transaction_type: string;
    model: string;
}

export interface IJob {
    job_id: number;
    job_name: string;
    run_type: string;
    parallel_count: number;
    create_date: string;
    modified_date: string;
    tolist: string;
    source_config: IJobconfig;
    dest_config: IJobconfig;
    map: Array<IJobmap>;
    sourcefields: Array<IJobFields>;
    destfields: Array<IJobFields>;
    models: Array<IJobModels>;

}
export interface IJobs {
    jobs: Array<IJob>;
}


export interface IJobsRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: IJobs;
}



export interface IJobModelRecord {
    models: Array<IJobModels>;
    fields: Array<IJobFields>;
}

export interface IJobModelRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: IJobModelRecord;
}

export var  initJobRecord: IJob = {
    job_id: -1, job_name: 'New', run_type: 'R',
    parallel_count: 1, create_date: null, modified_date: null,
    tolist: '',
    source_config: {
      job_id: -1,
      rec_type: 'S',
      conn_id: -1,
      conn_type: '',
      conn_name: '',
      conn_system_type: '',
      conn_logo_path: '/static/img/logo/dbgeneral.jpg',
      filepath: '',
      filestartwith: '',
      fileendwith: '',
      filemask: '',
      delimiter: '|',
      encoding: '',
      lineterminator: 'LF',
      archivepath: '',
      key_field: '',
      bulk_count: 1,
      transaction_type: '',
      model: '',
      query: {
        query: '', metadata: ''
      }
    }, dest_config: {
      job_id: -1,
      rec_type: 'D',
      conn_id: -1,
      conn_type: '',
      conn_name: '',
      conn_system_type: '',
      conn_logo_path: '/static/img/logo/dbgeneral.jpg',
      filepath: '',
      filestartwith: '',
      fileendwith: '',
      filemask: '',
      delimiter: '|',
      encoding: '',
      lineterminator: 'LF',
      archivepath: '',
      key_field: '',
      bulk_count: 1,
      transaction_type: '',
      model: '',
      query: {
        query: '', metadata: ''
      }

    }, map: [],
    sourcefields: [], destfields: [],
    models: []
  };
