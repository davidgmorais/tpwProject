import { Component, OnInit } from '@angular/core';
import {Item} from '../models/Item';
import {Category} from '../models/Category';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {

  discountedItems: Item[];
  biggestDiscount: number;
  newestItems: Item[];
  categories: Category[];
  constructor() { }

  ngOnInit(): void {
  }

}
