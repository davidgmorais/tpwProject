import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Item} from '../models/Item';
import {Category} from '../models/Category';
import {Comments} from '../models/Comments';

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class ItemsService {
  private apiURL = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) { }

  getItems(): Observable<Item[]> {
    const url = this.apiURL + 'item/';
    return this.http.get<Item[]>(url);
  }

  getItemsByCategory(category: string): Observable<any> {
    const url = this.apiURL + 'items/category/' + category;
    return  this.http.get<Item[]>(url);
  }

  getNewItems(): Observable<Item[]> {
    const url = this.apiURL + 'items/new';
    return this.http.get<Item[]>(url);
  }

  getPromoItems(): Observable<any> {
    const url = this.apiURL + 'items/promo';
    return this.http.get<Item[]>(url);
  }

  getItemInfo(id: number): Observable<Item> {
    const url = this.apiURL + 'item/' + id;
    return this.http.get<Item>(url);
  }

  getSearchResults(query: string): Observable<any> {
    const url = this.apiURL + 'search/' + query;
    return this.http.get<Item[]>(url);
  }

  getCategories(): Observable<Category[]> {
    const url = this.apiURL + 'category/';
    return this.http.get<Category[]>(url);
  }

  addCategory(token: string, category: string): Observable<any> {
    const url = this.apiURL + 'category/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    const body = {
      name: category,
      subcategories: []
    };
    return this.http.post(url, body, headers);
  }

  getItemComments(itemId: number): Observable<Comments[]> {
    const url = this.apiURL + 'comments/' + itemId  ;
    return this.http.get<Comments[]>(url);
  }

}
