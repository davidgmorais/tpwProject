import { Component, OnInit } from '@angular/core';
import {Item} from '../../models/Item';
import {Category} from '../../models/Category';
import {Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  items: Item[] = [];
  category: Category[] = [];
  pending: any = [];
  outOfStock: any = [];
  bestBuyers: any = [];

  constructor(private router: Router, private itemService: ItemsService) { }

  ngOnInit(): void {
    if (localStorage.getItem('username') !== 'admin') {
      this.router.navigateByUrl('/');
    }
    this.getCategories();
    this.getItems();
  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private getCategories(): void {
    this.itemService.getCategories().subscribe(response => {
      this.category = response.slice(0, 5);
    });
  }

  private getItems() {
    this.itemService.getNewItems().subscribe(response => {
      this.items = response.slice(0, 11);
    })
  }
}
