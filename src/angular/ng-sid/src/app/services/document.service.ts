import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { HOST_API } from '../app.config';
import { IDocumentRecords } from '../models/documents';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private localFileUrl = HOST_API + 'localdocument/';  // URL to web API
  private s3FileUrl = HOST_API + 's3document/';  // URL to web API

  constructor(private http: HttpClient) { }

  postDocument(fileToUpload: File, delimiter: string, lineterminator: string): Observable<IDocumentRecords> {
    const formData: FormData = new FormData();
    formData.append('document', fileToUpload, fileToUpload.name);
    formData.append('delimiter', delimiter);
    formData.append('lineterminator', lineterminator);

    return this.http.post<IDocumentRecords>(
      this.localFileUrl,
      formData
    );

  }

  s3Document(conn_id: string, filename: string, delimiter: string, lineterminator: string): Observable<IDocumentRecords> {
    const formData: FormData = new FormData();
    formData.append('conn_id', conn_id);
    formData.append('document', filename);
    formData.append('delimiter', delimiter);
    formData.append('lineterminator', lineterminator);

    return this.http.post<IDocumentRecords>(
      this.s3FileUrl,
      formData
    );

  }



}
