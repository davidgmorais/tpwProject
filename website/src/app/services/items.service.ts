import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Item} from '../models/Item';
import {Category} from '../models/Category';
import {Comments} from '../models/Comments';
import {Profile} from '../models/Profile';
import {Sell} from '../models/Sell';

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


  getItemComments(itemId: number): Observable<Comments[]> {
    const url = this.apiURL + 'comments/' + itemId  ;
    return this.http.get<Comments[]>(url);
  }


  // CATEGORIES
  // MAYBE CREATE CATEGORY SPECIFIC SERVICE

  getCategories(): Observable<Category[]> {
    const url = this.apiURL + 'category/';
    return this.http.get<Category[]>(url);
  }

  getCategory(categoryId: string): Observable<Category> {
    const url = this.apiURL + 'category/' + categoryId + '/';
    return this.http.get<Category>(url);
  }


  // ADMIN SERVICE
  // MAYBE CREATE ADMIN SPECIFIC SERVICE

  addItem(token: string, item: Item): Observable<any> {
    const url = this.apiURL + 'item/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.post(url, item, headers);
  }

  getDiscountStats(token: string): Observable<any>{
    const url = this.apiURL + 'admin/stats/discount';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get(url, headers);
  }

  getCategoryStats(token: string): Observable<any>{
    const url = this.apiURL + 'admin/stats/category';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get(url, headers);
  }

  getAgeStats(token: string): Observable<any>{
    const url = this.apiURL + 'admin/stats/age';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get(url, headers);
  }

  getBestBuyers(token: string): Observable<Profile[]> {
    const url = this.apiURL + 'admin/stats/bestbuyers';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get<Profile[]>(url, headers);
  }

  getOutOfStock(token: string): Observable<Item[]> {
    const url = this.apiURL + 'admin/outofstock';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get<Item[]>(url, headers);
  }

  getApproveList(token: string): Observable<Sell[]> {
    const url = this.apiURL + 'admin/purchases';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get<Sell[]>(url, headers);
  }

  declinePurchase(token: string, id: number): Observable<any> {
    const url = this.apiURL + 'admin/purchases/' + id + '/decline';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.put(url, {}, headers);
  }

  getPurchaseInfo(token: string, id: number): Observable<Sell> {
    const url = this.apiURL + 'sell/' + id;
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.get<Sell>(url, headers);
  }

  approvePurchase(token: string, id: number): Observable<any> {
    const url = this.apiURL + 'admin/purchases/' + id + '/approve';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.put(url, {}, headers);
  }

  addCategory(token: string, category: string): Observable<any> {
    const url = this.apiURL + 'category/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    const body = {
      name: category,
      parent: null,
      subcategories: [],
    };
    return this.http.post(url, body, headers);
  }

  editCategory(token: string, category: Category): Observable<any> {
    const url = this.apiURL + 'category/' + category.id + '/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.put(url, category, headers);
  }

  addSubcategory(token: string, category: string, parent: number): Observable<any> {
    const url = this.apiURL + 'category/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    const body = {
      name: category,
      subcategories: [],
      parent
    };
    return this.http.post(url, body, headers);
  }

  editSubcategory(token: string, category: Category): Observable<any> {
    const url = this.apiURL + 'category/' + category.id + '/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.put(url, category, headers);
  }

  deleteCategory(token: string, toDeleteId: number): Observable<any> {
    const url = this.apiURL + 'category/' + toDeleteId + '/delete/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.delete(url, headers);
  }

  upgradeItem(token: string, item: Item): Observable<any> {
    const url = this.apiURL + 'item/' + item.id;
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.put(url, item, headers);
  }

  deleteItem(token: string, itemId: number): Observable<any> {
    const url = this.apiURL + 'item/' + itemId + '/delete/';
    const headers = {headers: new HttpHeaders({'Content-Type': 'application/json', Authorization: 'Token ' + token})};
    return this.http.delete(url, headers);
  }

}
