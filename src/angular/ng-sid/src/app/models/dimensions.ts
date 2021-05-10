export interface IDimTransactionType {
    transaction_type: string;
    description: string;
}
export interface IDimDelimiterType {
    delimiter_type: string;
    description: string;
}
export interface IDimNewLineType {
    line_type: string;
    description: string;
}

export interface IDimFieldType {
    field_type: string;
    description: string;
}

export interface IDimMapType {
    map_type: string;
    description: string;
}

export interface IDimFileMask {
    filemask: string;
    conversion: string;
}

export interface IDimConnectors {
    conn_name: string;
    conn_type: string;
    conn_usage: string;
    conn_logo_path: string;
    description: string;
}

export interface IDimSystemTypes {
    system_type: string;
    description: string;
}


export interface IDimRef {
    dimconnectors: Array<IDimConnectors>;
    dimsystemtypes: Array<IDimSystemTypes>;
    dimfilemask: Array<IDimFileMask>;
    dimmaptype: Array<IDimMapType>;
    dimfieldtype: Array<IDimFieldType>;
    dimnewlinetype: Array<IDimNewLineType>;
    dimdelimitertype: Array<IDimDelimiterType>;
    dimtransactiontype: Array<IDimTransactionType>;

}


export interface IDimRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: IDimRef;
}
