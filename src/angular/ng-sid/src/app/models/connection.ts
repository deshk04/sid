import { ISFConnector } from '../models/salesforce';
import { IS3Connector } from '../models/awss3';

export interface IConnectorDetails {
    conn_id: number;
    name: string;
    conn_type: string;
    conn_system_type: string;
    conn_logo: string;
    create_date: string;
    modified_date: string;
    query_type: string;
    sfauth: ISFConnector;
    s3auth: IS3Connector;
}

export interface ISFAuth {
    id: number;
    name: string;
    auth_username: string;
    auth_password: string;
    auth_host: string;
    security_token: string;
    organisation_id: string;
    consumer_key: string;
}
export interface IS3Auth {
    id: number;
    name: string;
    aws_access_key_id: string;
    aws_secret_access_key: string;
    bucket_name: string;
    aws_region: string;

}

export interface IConnectors {
    id: number;
    name: string;
    conn_type: string;
    conn_system_type: string;
    conn_logo: string;
    create_date: string;
    modified_date: string;
}
export interface IConnections {
    connectors: Array<IConnectors>;
    sfauth: Array<ISFAuth>;
    s3auth: Array<IS3Auth>;
}


export interface IConnectionRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: IConnections;
}
