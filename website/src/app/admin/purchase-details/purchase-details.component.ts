import { Component, OnInit } from '@angular/core';
import {Sell} from '../../models/Sell';
import {ActivatedRoute, Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';

@Component({
  selector: 'app-purchase-details',
  templateUrl: './purchase-details.component.html',
  styleUrls: ['./purchase-details.component.css']
})
export class PurchaseDetailsComponent implements OnInit {

  token: string;
  details: Sell;
  profit: number;
  id: number;
  constructor(private route: ActivatedRoute, private itemService: ItemsService, private router: Router) { }

  ngOnInit(): void {
    this.token = localStorage.getItem('auth_token');
    this.getPurcahse();
  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private getPurcahse(): void {
    this.route.paramMap.subscribe(params => {
      this.id = +params.get('id');
      this.itemService.getPurchaseInfo(this.token, this.id).subscribe(response => {
        console.log(response);
        this.details = response;
        this.profit = this.details.moneyReceived - this.details.item.price;
      });
    });
  }

  approve(): void {
    this.itemService.approvePurchase(this.token, this.id).subscribe(response => {
      this.getPurcahse();
    });
  }

  deny(): void {
    this.itemService.declinePurchase(this.token, this.id).subscribe(response => {
      this.getPurcahse();
    });
  }
}
