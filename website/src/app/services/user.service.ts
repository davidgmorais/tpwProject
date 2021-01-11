import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiURL = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) {
  }

  login(username: string, password: string): Observable<any> {
    const url = this.apiURL + 'login';
    const body = {username, password};
    return this.http.post(url, body, httpOptions);
  }

}

