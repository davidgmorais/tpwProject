import { Component, OnInit } from '@angular/core';
import {Item} from '../../models/Item';
import {Category} from '../../models/Category';
import {Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';
import * as Chart from 'chart.js';
import {Profile} from '../../models/Profile';
import {Sell} from '../../models/Sell';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  items: Item[] = [];
  category: Category[] = [];
  pending: Sell[] = [];
  outOfStock: any = [];
  bestBuyers: Profile[] = [];
  bg: string[] = [];
  token: string;


  constructor(private router: Router, private itemService: ItemsService) { }

  ngOnInit(): void {
    if (localStorage.getItem('username') !== 'admin') {
      this.router.navigateByUrl('/');
    }
    this.token = localStorage.getItem('auth_token');
    this.getCategories();
    this.getItems();
    this.getBestBuyers();
    this.getOutOfStock();
    this.getApproveList();
  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private getCategories(): void {
    this.itemService.getCategories().subscribe(response => {
      this.category = response.slice(0, 5);

      // generate graph colors
      let range = response.length;
      if (range < 4) {
        range = 4;
      }
      for (let i = 0; i < range; i++) {
        this.bg.push('#' + ((1 << 24) * Math.random() | 0).toString(16));
      }

      // create graphs
      this.getDiscountStats();
      this.getCategoryStats();
      this.getAgeStats();

    });
  }

  private getItems(): void {
    this.itemService.getNewItems().subscribe(response => {
      this.items = response.results as Item[];
      this.items = this.items.slice(0, 11);
    });
  }

  private getDiscountStats(): void {
    this.itemService.getDiscountStats(this.token).subscribe(response => {
      const data = [response.Discounted, response.FullPrice];
      const labels = ['Discounted', 'FullPrice'];
      this.renderChart(data, labels, 'pieChart', 'pie');
    });
  }

  private getCategoryStats(): void {
    this.itemService.getCategoryStats(this.token).subscribe(response => {
      const data = [];
      const labels = [];
      for (const pair of response) {
        if (pair.parent !== undefined) {
          data.push(pair.purchases);
          labels.push(pair.name);
        }
      }
      this.renderChart(data, labels, 'catChart', 'pie');

    });
  }

  private getAgeStats(): void {
    this.itemService.getAgeStats(this.token).subscribe(response => {
      const labels = ['under 18', '18-40', '41-65', 'over 65'];
      const data = [];
      let index;
      for (const line of response) {
        index = labels.indexOf(line.AgeGroup);
        data[index] = line.purchases;
      }
      this.renderChart(data, labels, 'barChart', 'bar');
    });
  }

  private renderChart(data, labels, id, type): void {
    const canvas = document.getElementById(id) as HTMLCanvasElement;
    const ctx = canvas.getContext('2d');
    const myChart = new Chart(ctx, {
      type,
      data: {
        labels,
        datasets: [{
          label: 'data',
          data,
          backgroundColor: this.bg.slice(0, data.length)
        }]
      },
      options: {
        legend: {
          display: false
        }
      }
    });
  }

  private getBestBuyers(): void {
    this.itemService.getBestBuyers(this.token).subscribe(response => {
      this.bestBuyers = response;
    });
  }

  private getOutOfStock(): void {
    this.itemService.getOutOfStock(this.token).subscribe(response => {
      this.outOfStock = response;
    });
  }

  private getApproveList(): void {
    this.itemService.getApproveList(this.token).subscribe(response => {
      this.pending = response.filter(p => p.pendingSell);
    });
  }

  approve(id: number): void {
    this.itemService.approvePurchase(this.token, id).subscribe(response => {
      this.getApproveList();
    });
  }

  deny(id: number): void {
    this.itemService.declinePurchase(this.token, id).subscribe(response => {
      this.getApproveList();
    });
  }
}
