import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Category} from '../../models/Category';
import {ActivatedRoute, Router} from '@angular/router';
import {ItemsService} from '../../services/items.service';
import {Location} from '@angular/common';
import {invalid} from '@angular/compiler/src/render3/view/util';

@Component({
  selector: 'app-add-edit-subcategory',
  templateUrl: './add-edit-subcategory.component.html',
  styleUrls: ['./add-edit-subcategory.component.css']
})
export class AddEditSubcategoryComponent implements OnInit {
  action: string;
  id: string;
  token: string;
  subcategoryGroup: FormGroup;
  category: Category;
  categoryOptions = [];

  constructor(private fb: FormBuilder,
              private route: ActivatedRoute,
              private router: Router,
              private itemService: ItemsService,
              private location: Location) { }

  ngOnInit(): void {
    this.getAction();
    this.getId();
    this.populateOptions();

    this.token = localStorage.getItem('auth_token');
    this.createSubcategoryForm(this.id);
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
      if (this.action === 'edit' && !id) {
        this.router.navigateByUrl('/admin');
      } else {
        this.id = id;
      }
    });
  }


  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private createSubcategoryForm(categoryId: string): void {
    this.subcategoryGroup = this.fb.group({
      parent: new FormControl(null, Validators.required),
      name: new FormControl('', Validators.required)
    });

    if (categoryId && this.action === 'add') {
      this.itemService.getCategory(categoryId).subscribe( response => {
        this.category = response;
        this.subcategoryGroup.patchValue({parent: this.category.name});
      });
    } else if (categoryId && this.action === 'edit') {
      this.itemService.getCategories().subscribe(response => {
        const parentCategory = response.find(c => c.subcategories.find( sc => sc.id === +categoryId));
        this.category = parentCategory.subcategories.find(sc => sc.id === +categoryId);

        this.subcategoryGroup.setValue({name: this.category.name, parent: parentCategory.name});
      });
    }

  }

  addSubcategory(): void {
    if (this.subcategoryGroup.invalid) {
      return;
    }

    let parent;
    if (this.category) {
      parent = this.category.id;
    } else {
      parent = this.subcategoryGroup.value.parent;
    }

    this.itemService.addSubcategory(this.token, this.subcategoryGroup.value.name, parent).subscribe(response => {
      this.location.back();
    });

  }

  private populateOptions(): void {
    this.itemService.getCategories().subscribe(response => {
      for (const cat of response) {
        this.categoryOptions.push({value: cat.id, name: cat.name});
      }
    });
  }

  saveSubcategory(): void {
    if (this.subcategoryGroup.invalid) {
      return;
    }

    this.category.name = this.subcategoryGroup.value.name;

    this.itemService.editSubcategory(this.token, this.category).subscribe(response => {
      this.router.navigateByUrl('admin/category/edit/' + this.category.parent);
    });
  }
}
