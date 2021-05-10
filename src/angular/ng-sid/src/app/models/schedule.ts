import { IJob } from './jobs';
export interface ISchedule {
    id: number;
    schedule_type: string;
    schedule_name: string;
    frequency: string;
    day_of_week: string;
    day_of_month: string;
    hours:string;
    minutes: string;
    create_date: string;
    modified_date: string;

}
export interface IScheduleConfig {
    id: number;
    job_sequence: number;
    job_id: number;
    job_name: string;
    run_type: string;
}

export interface IScheduleDistribution {
    id: number;
    email_flag: string;
    tolist: string;
    cclist: string;
    bcclist: string;
}


export interface ISchedules {
    schedules: Array<ISchedule>;
    scheduleconfig: Array<IScheduleConfig>;
}

export interface IScheduleRecords {
    status: string;
    message: string;
    num_of_records: number;
    records: ISchedules;
}

export interface IScheduleSelect {
    schedules: ISchedule;
    scheduleconfig: Array<IScheduleConfig>;
    distribution: IScheduleDistribution;
}

export interface IScheduleRecordById {
    status: string;
    message: string;
    num_of_records: number;
    records: IScheduleSelect;
}


export interface IScheduleJobrun {
    job_id:        number;
    run_date:      string;
    message:       string;
    status:        string;
    success_count: number | null;
    failure_count: number | null;
    warning_count: number | null;
    total_count:   number | null;
    jobrun_id:     number;
    job_name:      string;
    start_date:    string;
    end_date:      string;
}

export interface ISchedulelog {
    schedule_id:    number;
    run_date:       string;
    message:        string;
    status:         string;
    schedulelog_id: number;
    start_date:     string;
    end_date:       string;
    jobrun:         Array<IScheduleJobrun>;
}


// export interface IScheduleLogRecord {
//     schedulelogs: ISchedulelog;
// }

export interface IScheduleLogRecords {
    status:         string;
    message:        Array<string>;
    num_of_records: number;
    records:        Array<ISchedulelog>;
}


export var  initScheduleRecord: IScheduleSelect = {
    schedules: {
            id: -1,
            schedule_type: 'R',
            schedule_name: '',
            frequency: 'Daily',
            create_date: '',
            modified_date: '',
            day_of_week: '',
            day_of_month: '',
            hours: '',
            minutes: ''
    },
    scheduleconfig: [],
    distribution: {
        id: -1,
        email_flag: '',
        tolist: '',
        cclist: '',
        bcclist: ''
    }
};