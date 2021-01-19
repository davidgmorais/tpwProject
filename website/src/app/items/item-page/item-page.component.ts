import { Component, OnInit } from '@angular/core';
import {ItemsService} from '../../services/items.service';
import {ActivatedRoute} from '@angular/router';
import {Item} from '../../models/Item';
import {Comments} from '../../models/Comments';

@Component({
  selector: 'app-item-page',
  templateUrl: './item-page.component.html',
  styleUrls: ['./item-page.component.css']
})
export class ItemPageComponent implements OnInit {

  item: Item;
  comments: Comments[];
  userIsAuthenticated: string;

  constructor(private route: ActivatedRoute, private itemService: ItemsService) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.getItem(id);
    this.getComments(id);
  }

  private getItem(id: string): void {
    this.itemService.getItemInfo(+id).subscribe(response => {
      this.item = response;
    });
  }

  private getComments(id: string): void {
    this.itemService.getComments().subscribe(response => {
      this.comments = response.filter(i => i.item.id === +id);
    });
    // this.itemService.getItemComments(+id).subscribe(response => {
    //   this.comments = response;
    // });
  }

  addToCart(): void {

  }

  sellItem(): void {

  }
}
