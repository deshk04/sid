export interface IObject {
    object_id: number;
    object_type: string;
    first_name: string;
    middle_name: string;
    last_name: string;
    stem: string;
    practice_name: string;
    ahpra_number: string;
    provider_number: string;
}


export interface IObjectRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: Array<IObject>;
}
