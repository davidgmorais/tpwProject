import { Component, OnInit } from '@angular/core';
import {Item} from '../../models/Item';
import {ActivatedRoute, Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';
import {Category} from '../../models/Category';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-item-list',
  templateUrl: './item-list.component.html',
  styleUrls: ['./item-list.component.css']
})
export class ItemListComponent implements OnInit {

  items: Item[] = [];
  title: string;
  category: Category;
  filterGroup: FormGroup;
  brandList = [];
  currentPage = 1;
  totalItems: number;
  maxPage: number;

  ratingList = [
    {value: 1, name: '1 star'},
    {value: 2, name: '2 stars'},
    {value: 3, name: '3 stars'},
    {value: 4, name: '4 stars'},
    {value: 5, name: '5 stars'}
  ];
  sortChoices = [
    {value: '1', name: 'New'},
    {value: '2', name: 'Price Ascending'},
    {value: '3', name: 'Price Descending'},
    {value: '4', name: 'Best Sellers'},
    {value: '5', name: 'Biggest Discount'}
  ];
  filterString = '?';

  constructor(private route: ActivatedRoute, private router: Router, private itemService: ItemsService, private fb: FormBuilder) { }

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
        const categoryId = params.get('slug');
        if (categoryId) {
          this.getCategory(categoryId);

        } else {
          this.router.navigateByUrl('/');
        }

      } else {
        this.router.navigateByUrl('/');
      }

      this.createFilters();
    });

  }

  getAllItems(page: number = 1, filters: string = null): void {
    this.itemService.getItemList(page, filters).subscribe(response => {
      this.totalItems = response.count;
      this.maxPage = Math.ceil(this.totalItems / 16);
      this.items = response.results as Item[];
    });
  }

  isNew(item: Item): boolean {
    const dateThreshold = new Date(new Date().getTime() - (7 * 24 * 60 * 60 * 1000));
    return new Date(item.insertDate) > dateThreshold;
  }

  private getCategory(categoryId): void {
    this.itemService.getCategory(categoryId).subscribe(response => {
      this.category = response;
      this.title = this.category.name;
      this.getItemsByCategory(this.category.slug);

    });
  }

  private getPromoItems(page: number = 1, filters: string = null): void {
    this.itemService.getPromoItems(page, filters).subscribe(response => {
      this.totalItems = response.count;
      this.maxPage = Math.ceil(this.totalItems / 16);
      this.items = response.results as Item[];
    });
  }

  private getNewItems(page: number = 1, filters: string = null): void {
    this.itemService.getNewItems(page, filters).subscribe(response => {
      this.totalItems = response.count;
      this.maxPage = Math.ceil(this.totalItems / 16);
      this.items = response.results as Item[];    });
  }

  private getItemsByCategory(categorySlug: string, page: number = 1, filters: string = null): void {
    this.itemService.getItemsByCategory(categorySlug, page, filters).subscribe(response => {
      this.totalItems = response.count;
      this.maxPage = Math.ceil(this.totalItems / 16);
      this.items = response.results as Item[];
    });
  }

  private createFilters(): void {
    this.filterGroup = this.fb.group({
      order: new FormControl(    null),
      min: new FormControl(''),
      max: new FormControl(''),
      brand: new FormControl(null),
      availability: new FormControl(null),
      discount: new FormControl(null),
      reviews: new FormControl(null),
    });

    this.populateBrandList();
  }

  private populateBrandList(): void {
    this.itemService.getBrands().subscribe(response => {
      this.brandList = response;
    });
  }

  filter(): void {
    this.filterString = '?';
    Object.keys(this.filterGroup.controls).forEach(key => {
      if (this.filterGroup.controls[key].value !== null) {
        this.filterString += key + '=' + this.filterGroup.controls[key].value + '&';
      }
    });

    if (this.title === 'All items') {
      this.getAllItems(this.currentPage, this.filterString);

    } else if (this.title === 'New in') {
      this.getNewItems(this.currentPage, this.filterString);

    } else if (this.title === 'Promos') {
      this.getPromoItems(this.currentPage, this.filterString);

    } else {
      this.getItemsByCategory(this.category.slug, this.currentPage, this.filterString);
    }
  }

  clear(): void {
    this.filterGroup.reset();
    this.filter();
  }

  goToPage(page: number): void {
    if (this.title === 'All items') {
      this.getAllItems(page, this.filterString);

    } else if (this.title === 'New in') {
      this.getNewItems(page, this.filterString);

    } else if (this.title === 'Promos') {
      this.getPromoItems(page, this.filterString);

    } else {
      this.getItemsByCategory(this.category.slug, page, this.filterString);
    }
  }

  previousPage(): void {
    this.currentPage--;
    this.goToPage(this.currentPage);
  }

  firstPage(): void {
    this.currentPage = 1;
    this.goToPage(1);
  }

  nextPage(): void {
    this.currentPage++;
    this.goToPage(this.currentPage);
  }

  lastPage(): void {
    this.currentPage = this.maxPage;
    this.goToPage(this.currentPage);
  }
}
