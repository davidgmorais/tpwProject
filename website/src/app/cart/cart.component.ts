import { Component, OnInit } from '@angular/core';
import {Cart} from '../models/Cart';
import {OrderItem} from '../models/OrderItem';
import {Profile} from '../models/Profile';
import {ItemsService} from '../services/items.service';
import {ActivatedRoute, Router} from '@angular/router';
import {UserService} from '../services/user.service';
import {Purchase} from '../models/Purchase';
import {Item} from '../models/Item';

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
  itemList: Item[] = [];
  subtotal: number;
  item: Item;

  constructor(private route: ActivatedRoute, private router: Router, private itemService: ItemsService,
              private userService: UserService) {
    this.token = localStorage.getItem('auth_token');
    this.username = localStorage.getItem('username');
  }

  ngOnInit(): void {
    this.getProfile();
  }

  private getProfile(): void {
    this.userService.getAccounts().subscribe(response => {
      this.profile = response.find(i => i.user.username === this.username);
      this.getCart();
    });
  }

  private getCart(): void {
    this.itemService.getCart().subscribe(response => {
      this.cart = response.find(i => i.user === this.profile.id);
      this.getOrderItems();
    });
  }

  private getOrderItems(): void {
    this.itemService.getOrderItems().subscribe(response => {
      this.orderedItems = response.filter(i => i.cart === this.cart.id);
      this.fillItems();
    });
  }

  private fillItems(): void {
    this.subtotal = 0;
    this.itemService.getItems().subscribe(response => {
      for (const oItem of this.orderedItems ) {
        oItem.item = response.find(i => i.id === oItem.item);
      }
      console.log(this.subtotal);
      this.getTotal();
    });
  }

  private getTotal(): void {
    for (const order of this.orderedItems){
      this.subtotal += (order.item.price - ((order.item.price * order.item.discount) / 100)) * order.qty;
    }
    this.total = this.subtotal;
    if (this.profile.money >= this.subtotal){
      this.total = 0;
    }
    if (this.profile.money < this.subtotal){
      this.total = this.subtotal - this.profile.money;
    }
  }

  removeItem(orderId: number): void {
    this.orderedItems.filter(i => i.id !== orderId);
    this.itemService.deleteOrderItem(orderId).subscribe(response => {
      this.router.navigateByUrl('/cart');
      this.getOrderItems();
    });
  }

  decreaseOrderQty(orderId: number): void {
    const updateOrder = this.orderedItems.find(i => i.id === orderId);
    const index = this.orderedItems.indexOf(updateOrder);
    this.orderedItems[index].qty -= 1;
    this.orderedItems[index].item = this.orderedItems[index].item.id;
    this.itemService.updateOrderItem(orderId, updateOrder).subscribe(response => {
      this.getOrderItems();
    });
  }

  increaseOrderQty(orderId: number): void {
    const updateOrder = this.orderedItems.find(i => i.id === orderId);
    const index = this.orderedItems.indexOf(updateOrder);
    this.orderedItems[index].qty += 1;
    this.orderedItems[index].item = this.orderedItems[index].item.id;
    this.itemService.updateOrderItem(orderId, updateOrder).subscribe(response => {
      this.getOrderItems();
    });
  }

  purchaseCart(): void{
    for (const order of this.orderedItems){
      // order.item = order.item.id;
      this.itemService.purchaseItem(this.token, order.item).subscribe(response => {
        this.itemService.deleteOrderItem(order.id).subscribe();
      });
    }
    this.profile.money = 0;
    this.userService.updateAccount(this.profile, this.profile.id).subscribe( response => {
      this.router.navigateByUrl('/');
    });
  }
}
