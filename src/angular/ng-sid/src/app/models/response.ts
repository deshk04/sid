
export interface IResponseRecord {
  field_name: string;
  message: string;
}

export interface IResponse {
  num_of_pages: number;
  status: string;
  message: Array<string>;
  num_of_records: number;
  records: Array<IResponseRecord>;
}
