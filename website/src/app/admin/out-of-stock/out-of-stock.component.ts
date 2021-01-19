import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Item} from '../../models/Item';
import {ItemsService} from '../../services/items.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-out-of-stock',
  templateUrl: './out-of-stock.component.html',
  styleUrls: ['./out-of-stock.component.css']
})
export class OutOfStockComponent implements OnInit {
  token: string;
  id: number;
  item: Item;
  table: Item[] = [];
  quantityGroup: FormGroup;
  errorMsg: string;
  constructor(private route: ActivatedRoute, private router: Router, private itemsService: ItemsService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.token = localStorage.getItem('auth_token');
    this.getId();
  }

  private getId(): void {
    this.route.paramMap.subscribe(params => {

      if (params.get('id')){
        const id = +params.get('id');
        if (isNaN(id)) {
          this.router.navigateByUrl('/admin');
        }
        this.id = id;
        this.getItem();
        this.createForm();

      } else {
        this.getOutOfStockItems();
      }
    });
  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private getOutOfStockItems(): void {
    this.itemsService.getOutOfStock(this.token).subscribe(response => {
      this.table = response;
    });

  }

  private getItem(): void {
    this.itemsService.getItemInfo(this.id).subscribe(response => {
      this.item = response;
      if (this.item.quantity !== 0) {
        this.router.navigateByUrl('/admin/outofstock');
      }
    });
  }

  private createForm(): void {
    this.quantityGroup = this.fb.group({
      quantity: ['0', [Validators.required, Validators.min(1)]]
    });
  }

  upgradeQuantity(): void {
    if (this.quantityGroup.invalid) {
      this.errorMsg = 'Quantity must bigger than 0';
      return;
    }
    this.errorMsg = null;
    this.item.quantity = this.quantityGroup.value.quantity;
    this.item.picture = undefined;
    this.itemsService.upgradeItem(this.token, this.item).subscribe(response => {
      this.router.navigateByUrl('/admin/outofstock');
    });

  }
}
