import {HttpClient, HttpParams} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable()
export class DataFetcher {
    constructor(private http: HttpClient) {}

    fetch(url: string, opts?: any, body?: any): Observable<any> {
        let params = new HttpParams();
        const queryOpts = { ...opts, params };
        switch (opts?.req) {
            case 'delete':
                return this.http.delete<any>(url, queryOpts);
            case 'put':
                return this.http.put<any>(url, body, queryOpts);
            case 'post':
                return this.http.post<any>(url, body, queryOpts);
            case 'head':
                return this.http.head<any>(url, queryOpts);
            case 'patch':
                return this.http.patch<any>(url, body, queryOpts);
            default:
                return this.http.get<any>(url, queryOpts);
        }
    }
}
