import { IJobFields, IJobconfig } from './jobs';
export interface IDocument {
  field_name: string;
  field_type: string;
  field_length: string;
  field_format: string;
  label: string;
  primary_key: string;
}

export interface IDocumentRecord {
  document: Array<IJobFields>;
  config: IJobconfig;
}


export interface IDocumentRecords {
  status: string;
  message: Array<string>;
  num_of_records: number;
  records: IDocumentRecord;
}
