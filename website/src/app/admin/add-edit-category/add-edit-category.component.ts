import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';
import {Category} from '../../models/Category';

@Component({
  selector: 'app-add-edit-category',
  templateUrl: './add-edit-category.component.html',
  styleUrls: ['./add-edit-category.component.css']
})
export class AddEditCategoryComponent implements OnInit {
  action: string;
  id: string;
  token: string;
  itemGroup: FormGroup;
  category: Category;
  toDeleteId: number;

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router, private itemService: ItemsService) { }

  ngOnInit(): void {
    this.getAction();
    this.getId();
    this.createCategoryForm(this.id);

    this.token = localStorage.getItem('auth_token');

  }

  private getAction(): void {
    this.route.paramMap.subscribe(params => {
      const action = params.get('action');
      if (action === 'edit') {
        this.action = 'edit';
      } else if (action === 'add') {
        this.action = 'add';
      } else {
        this.router.navigateByUrl('/admin');
      }
    });
  }

  private getId(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (this.action === 'add' && id) {
        this.router.navigateByUrl('/admin');
      } else if (this.action === 'edit' && !id) {
        this.router.navigateByUrl('/admin');
      } else {
        this.id = id;
      }
    });
  }

  private createCategoryForm(categoryId: string): void {
    this.itemGroup = this.fb.group({
      name: new FormControl('', Validators.required)
    });

    if (categoryId) {
      this.itemService.getCategory(categoryId).subscribe( response => {
        this.category = response;
        this.itemGroup.patchValue({name: this.category.name});
      });
    }

  }

  addCategory(): void {
    if (this.itemGroup.invalid) {
      return;
    }

    const name = this.itemGroup.value.name;
    this.itemService.addCategory(this.token, name).subscribe(response => {
      this.router.navigateByUrl('admin/category');
    });

  }

  editCategory(): void {
    if (this.itemGroup.invalid) {
      return;
    }

    this.category.name = this.itemGroup.value.name;
    this.category.subcategories = [];

    this.itemService.editCategory(this.token, this.category).subscribe(response => {
      this.router.navigateByUrl('admin/category');
    });

  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  deleteCategory(): void {
    this.itemService.deleteCategory(this.token, this.toDeleteId).subscribe(response => {
      console.log(response);
      if (this.toDeleteId === this.category.id) {
        this.router.navigateByUrl('/admin/category');
      } else {
        this.toDeleteId = null;
        this.createCategoryForm(this.id);
      }
    });
  }

  toDelete(id: number = null): void {
    this.toDeleteId = id;
  }
}
