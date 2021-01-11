import { Component, OnInit } from '@angular/core';
import {Cart} from '../models/Cart';
import {Category} from '../models/Category';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';
import {Router} from '@angular/router';
import {ItemsService} from '../services/items.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  userIsAuthenticated: string;
  cart: Cart;
  categories: Category[];
  searchForm: FormGroup;

  constructor(private router: Router, private fb: FormBuilder, private itemService: ItemsService) { }

  ngOnInit(): void {
    this.searchForm = this.fb.group({
      query: ['']
    });
    this.getCategories();
    this.userIsAuthenticated = localStorage.getItem('auth_token');
  }

  search(): void {
    const query = this.searchForm.value.query;
    this.router.navigateByUrl('/search?q=' + query);
  }

  getCategories(): void {
    this.itemService.getCategories().subscribe(response => {
      this.categories = response;
    });
  }
}
