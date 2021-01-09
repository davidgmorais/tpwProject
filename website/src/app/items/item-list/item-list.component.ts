import { Component, OnInit } from '@angular/core';
import {Item} from '../../models/Item';
import {ActivatedRoute, Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';
import {Category} from '../../models/Category';

@Component({
  selector: 'app-item-list',
  templateUrl: './item-list.component.html',
  styleUrls: ['./item-list.component.css']
})
export class ItemListComponent implements OnInit {

  items: Item[];
  title: string;
  category: Category;
  constructor(private route: ActivatedRoute, private router: Router, private itemService: ItemsService) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      if (!params.get('id')) {
        this.title = 'All items';
        this.getAllItems();

      } else if (params.get('id') === 'new') {
        this.title = 'New in';
        this.getNewItems();

      } else if (params.get('id') === 'promo') {
        this.title = 'Promos';
        this.getPromoItems();

      } else if (params.get('id') === 'category') {
        const categorySlug = params.get('slug');
        if (categorySlug) {
          this.getCategory(categorySlug);
          this.getItemsByCategory(categorySlug);

        } else {
          this.router.navigateByUrl('');
        }

      } else {
        this.router.navigateByUrl('');
      }
    });

  }

  getAllItems(): void {
    this.itemService.getItems().subscribe(response => {
      this.items = response;
    });
  }

  isNew(item: Item): boolean {
    const dateThreshold = new Date(new Date().getTime() - (7 * 24 * 60 * 60 * 1000));
    return new Date(item.insertDate) > dateThreshold;
  }

  private getCategory(slug): void {
    this.itemService.getCategories().subscribe(response => {
      this.category = response.find(c => c.slug === slug);
      this.title = this.category.name;
    });
  }

  private getPromoItems(): void {
    this.itemService.getPromoItems().subscribe(response => {
      this.items = response;
    });
  }

  private getNewItems(): void {
    this.itemService.getNewItems().subscribe(response => {
      this.items = response;
    });
  }

  private getItemsByCategory(categorySlug: string): void {
    this.itemService.getItemsByCategory(categorySlug).subscribe(response => {
      this.items = response;
    })

  }
}
