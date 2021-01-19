import { Component, OnInit } from '@angular/core';
import {Sell} from '../../models/Sell';
import {ItemsService} from '../../services/items.service';

@Component({
  selector: 'app-approve-purchases',
  templateUrl: './approve-purchases.component.html',
  styleUrls: ['./approve-purchases.component.css']
})
export class ApprovePurchasesComponent implements OnInit {

  purchases: Sell[] = [];
  token: string;
  constructor(private itemsService: ItemsService) { }

  ngOnInit(): void {
    this.token = localStorage.getItem('auth_token');
    this.getApproveList();
  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private getApproveList(): void {
    this.itemsService.getApproveList(this.token).subscribe(response => {
      this.purchases = response;
    });
  }

  approve(id: number): void {
    this.itemsService.approvePurchase(this.token, id).subscribe(response => {
      this.getApproveList();
    });
  }

  deny(id: number): void {
    this.itemsService.declinePurchase(this.token, id).subscribe(response => {
      this.getApproveList();
    });
  }
}
