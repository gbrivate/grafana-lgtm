// document-sign.service.ts
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SignService {
  constructor(private http: HttpClient) {}

  signDocument(content: string) {
    // Define headers to tell the server we are sending plain text
    const headers = new HttpHeaders({ 'Content-Type': 'text/plain' });
    return this.http.post('http://localhost/fastapi/sign-document', content, { headers, responseType: 'text' });
  }

  verifyDocument(signature:string, originalString:string){
    const headers = new HttpHeaders({
      'Content-Type': 'text/plain',
      'X-Signature': signature // A string Base64 que você recebeu do /sign-document
    });

    return this.http.post('http://localhost/fastapi/verify-document', originalString, { headers });
  }
}
