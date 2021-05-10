export interface IFields {
    model_id: number,
    field_name: string;
    field_type: string;
    field_length: string;
    field_format: string;
    label: string;
    primary_key: string;
}

export interface IModel {
    id: number;
    conn_id: number;
    name: string;
    label: number;
    readable: string;
    writeable: string;
}

export interface IModelmap {
    job_id: number;
    source_model: string;
    source_field: string;
    map_type: string;
    map_value: string;
    lookup_model: string;
    lookup_join_field: string;
    lookup_return_field: string;
    dest_model: string;
    dest_field: string;
    create_date: string;
    modified_date: string;
}
export interface IModels {
    fields: Array<IFields>;
    model: Array<IModel>;
    map: Array<IModelmap>;
}

export interface IModelRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: IModels;
}
