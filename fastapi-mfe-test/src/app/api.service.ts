import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const BASE_URL = 'http://localhost/fastapi';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) {}

  slow(delay: number): Observable<any> {
    return this.http.get(`${BASE_URL}/slow`, {
      mode: 'no-cors',
      params: { timeDelay: delay }
    });
  }

  rollDice(player?: string): Observable<any> {
    return this.http.get(`${BASE_URL}/rolldice`, {
      mode: 'no-cors',
      params: player ? { player } : {}
    });
  }

  hello(name: string): Observable<any> {
    return this.http.get(`${BASE_URL}/hello`, {
      mode: 'no-cors',
      params: { name }
    });
  }

  error(code: number): Observable<any> {
    return this.http.get(`${BASE_URL}/error`, {
      mode: 'no-cors',
      params: { code }
    });
  }

  callLoop(loop: number): Observable<any> {
    return this.http.get(`${BASE_URL}/call-loop`, {
      mode: 'no-cors',
      params: { loop }
    });
  }

  callJava(): Observable<any> {
    return this.http.get(`http://localhost/java/api/hello`, {
      mode: 'no-cors',
    });
  }


}
