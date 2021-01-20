import { Component, OnInit } from '@angular/core';
import {ItemsService} from '../../services/items.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Item} from '../../models/Item';
import {Comments} from '../../models/Comments';
import {Cart} from '../../models/Cart';
import {Profile} from '../../models/Profile';
import {UserService} from '../../services/user.service';
import {OrderItem} from '../../models/OrderItem';

@Component({
  selector: 'app-item-page',
  templateUrl: './item-page.component.html',
  styleUrls: ['./item-page.component.css']
})
export class ItemPageComponent implements OnInit {

  profile: Profile;
  cart: Cart;
  item: Item;
  orderItem: OrderItem;
  comments: Comments[] = [];
  userIsAuthenticated: string;
  token: string;
  username: string;

  constructor(private route: ActivatedRoute, private router: Router, private itemService: ItemsService, private userService: UserService) {
    this.userIsAuthenticated = localStorage.getItem('username');
    this.token = localStorage.getItem('auth_token');
    this.username = localStorage.getItem('username');
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.getProfile();
    this.getItem(id);
    this.getComments(id);
  }

  private getProfile(): void {
    this.userService.getAccounts().subscribe(response => {
      this.profile = response.filter(i => i.user.username === this.username)[0];
    });
  }

  private getItem(id: string): void {
    this.itemService.getItemInfo(+id).subscribe(response => {
      this.item = response;
    });
  }

  private getComments(id: string): void {
    this.itemService.getComments().subscribe(response => {
      this.comments = response.filter(i => i.item === +id);
    });
  }

  addToCart(): void {
    this.itemService.getCart(this.token).subscribe(response => {
      this.cart = response.filter(i => i.user.id === this.profile.id)[0];
    });
    this.itemService.orderItem(this.token, this.cart, this.item).subscribe(response => {
      this.router.navigateByUrl('/');
    });
  }

  sellItem(): void {
    this.itemService.sellItem(this.token, this.profile, this.item).subscribe(response => {
      this.router.navigateByUrl('/account');
    });
  }
}
