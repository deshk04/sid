import { IConnectorDetails } from './connection';
import { IJobFields, IJobModels, IJobquery } from './jobs';
export interface ISFConnector {
    // query_type: string;
    // conn_id: number;
    // name: string;
    // conn_type: string;
    // conn_system_type: string;
    auth_username: string;
    auth_password: string;
    auth_host: string;
    security_token: string;
    oauth_object_id: string;
}

// export interface ISFConnections {
//     connection: Array<ISFConnector>;
// }

// export interface ISFConnectionRecords {
//     status: string;
//     message: string;
//     num_of_records: number;
//     records: Array<ISFConnections>;
// }

export interface ISFQueryResult {
    fields: Array<IJobFields>;
    records: [];
    filedata: any;
    filename: string;
}

export interface ISFVerifyQueryRecords {
    status: string;
    message: string;
    num_of_records: number;
    records: ISFQueryResult;
}


export interface ISFParsedQuery {
    fields: Array<IJobFields>;
    models: Array<IJobModels>;
    model_name: string;
    query: IJobquery
    connector: IConnectorDetails
    filter: string;
    download: string;
}


export var initsfjob: ISFParsedQuery = {
    fields: [],
    models: [],
    model_name: '',
    query: {
      query: '', metadata: ''
    },
    connector: {
      conn_id: -1,
      name: '',
      conn_type: '',
      conn_system_type: '',
      conn_logo: '',
      create_date: '',
      modified_date: '',
      query_type: '',
      sfauth: null,
      s3auth: null

    },
    filter: '',
    download: ''
  }
