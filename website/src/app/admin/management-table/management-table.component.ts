import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';

@Component({
  selector: 'app-management-table',
  templateUrl: './management-table.component.html',
  styleUrls: ['./management-table.component.css']
})
export class ManagementTableComponent implements OnInit {
  type: string;
  toDeleteId: number;
  table: any = [];
  token: string;

  constructor(private router: Router, private route: ActivatedRoute, private itemService: ItemsService) { }

  ngOnInit(): void {

    this.route.paramMap.subscribe(params => {
      const type = params.get('type');
      if (type === 'item') {
        this.type = 'item';
        this.getItems();
      } else if (type === 'category') {
        this.type = 'category';
        this.getCategories();
      } else {
        this.router.navigateByUrl('/admin');
      }
    });
    this.token = localStorage.getItem('auth_token');

  }

  private getItems(): void {
    this.itemService.getItems().subscribe(response => {
      console.log(response)
      this.table = response;
    });
  }

 private getCategories(): void {
    this.itemService.getCategories().subscribe(response => {
      this.table = response;
    });

  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  toDelete(id: number = null): void {
    this.toDeleteId = id;
  }

  deleteCategory(): void {
    this.itemService.deleteCategory(this.token, this.toDeleteId).subscribe(response => {
      this.toDeleteId = null;
      this.getCategories();
    });
  }

  deleteItem(): void {
    this.itemService.deleteItem(this.token, this.toDeleteId).subscribe(response => {
      this.toDeleteId = null;
      this.getItems();
    });
  }
}
