import { Component, OnInit } from '@angular/core';
import {Cart} from '../models/Cart';
import {OrderItem} from '../models/OrderItem';
import {Profile} from '../models/Profile';
import {ItemsService} from '../services/items.service';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../services/user.service';
import {Purchase} from '../models/Purchase';

@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {
  cart: Cart;
  orderedItems: OrderItem[] = [];
  profile: Profile;
  token: string;
  username: string;
  purchase: Purchase;
  total: number;

  constructor(private route: ActivatedRoute, private router: Router, private itemService: ItemsService,
              private userService: UserService) {
    this.token = localStorage.getItem('auth_token');
    this.username = localStorage.getItem('username');
  }

  ngOnInit(): void {
    this.getProfile();
    this.getCart();
    this.getOrderItems();
    this.getTotal();
  }

  private getProfile(): void {
    this.userService.getAccounts().subscribe(response => {
      this.profile = response.filter(i => i.user.username === this.username)[0];
    });
  }

  private getCart(): void {
    this.itemService.getCart().subscribe(response => {
      this.cart = response.filter(i => i.user === this.profile.id)[0];
    });
  }

  private getOrderItems(): void {
    this.itemService.getOrderItems().subscribe(response => {
      this.orderedItems = response.filter(i => i.cart.id === this.cart.id);
    });
  }

  private removeItem(orderId: number): void {
  }

  private decreaseOrderQty(orderId: number): void {
  }

  private increaseOrderQty(orderId: number): void {
  }

  private getTotal(): void {

  }

  private purchaseCart(): void{

}

}
