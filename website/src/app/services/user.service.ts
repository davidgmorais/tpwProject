import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import { Profile } from '../models/Profile';
import { Comments } from '../models/Comments';
import {Purchase} from '../models/Purchase';
import {Sell} from '../models/Sell';
import {Item} from '../models/Item';
import {Category} from '../models/Category';

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

  register(profile: Profile): Observable<any> {
    const url = this.apiURL + 'profiles/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json'})};
    return this.http.post(url, profile, headers);
  }

  getAccounts(): Observable<Profile[]> {
    const url = this.apiURL + 'profiles/';
    return this.http.get<Profile[]>(url);
  }

  updateAccount(money: number, id: number): Observable<any> {
    const url = this.apiURL + 'profiles/' + id;
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json'})};
    return this.http.put(url, money, headers);
  }

  getComments(): Observable<Comments[]> {
    const url = this.apiURL + 'comment/';
    return this.http.get<Comments[]>(url);
  }

  getPurchases(): Observable<Purchase[]> {
    const url = this.apiURL + 'purchase/';
    return this.http.get<Purchase[]>(url);
  }

  getSells(): Observable<Sell[]> {
    const url = this.apiURL + 'sell/';
    return this.http.get<Sell[]>(url);
  }

  getItems(): Observable<Item[]> {
    const url = this.apiURL + 'item/all';
    return this.http.get<Item[]>(url);
  }

  getCommentInfo(commentId: number): Observable<Comments> {
    const url = this.apiURL + 'comment/' + commentId;
    return this.http.get<Comments>(url);
  }

  addComment(comment: Comments): Observable<any> {
    const url = this.apiURL + 'comment/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json'})};
    return this.http.post(url, comment, headers);
  }

  editComment(comment: Comments): Observable<any> {
    const url = this.apiURL + 'comment/' + comment.id;
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json'})};
    return this.http.put(url, comment, headers);
  }

  deleteComment(commentId: number): Observable<any> {
    const url = this.apiURL + 'comment/' + commentId + '/delete';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json'})};
    return this.http.delete(url, headers);
  }

}

