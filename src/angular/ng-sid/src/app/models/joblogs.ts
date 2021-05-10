export interface IJoblogRec {
    job_id: number;
    jobrun_id: number;
    job_name: string;
    run_type: string;
    filename: string;
    file_date: string;
    run_date: string;
    message: string;
    status: string;
    start_date: string;
    end_date: string;
    success_count: number;
    failure_count: number;
    warning_count: number;
    total_count: number;
}
export interface Ijoblogs {
    joblogs: Array<IJoblogRec>;
}


export interface IJoblogsRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: Ijoblogs;
}
