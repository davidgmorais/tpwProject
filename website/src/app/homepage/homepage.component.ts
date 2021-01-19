import { Component, OnInit } from '@angular/core';
import {Item} from '../models/Item';
import {Category} from '../models/Category';
import {ItemsService} from '../services/items.service';
import {max} from 'rxjs/operators';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {

  discountedItems: Item[] = [];
  biggestDiscount: number;
  newestItems: Item[] = [];
  categories: Category[] = [];

  constructor(private itemService: ItemsService) { }

  ngOnInit(): void {
    this.getPromos();
    this.getNew();
  }

  private getPromos(): void {
    this.itemService.getPromoItems().subscribe(response => {
      this.discountedItems = response.slice(0, 4);
      if (this.discountedItems.length > 0) {
        this.biggestDiscount = this.discountedItems.find( x => Math.max(x.discount)).discount;
      }
    });
  }

  isNew(item: Item): boolean {
    const dateThreshold = new Date(new Date().getTime() - (7 * 24 * 60 * 60 * 1000));
    return new Date(item.insertDate) > dateThreshold;
  }

  private getNew(): void {
    this.itemService.getNewItems().subscribe(response => {
      this.newestItems = response.slice(0, 4);
    });
  }

}
