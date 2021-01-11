import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {Category} from '../../models/Category';
import {ItemsService} from '../../services/items.service';
import {Item} from '../../models/Item';

@Component({
  selector: 'app-add-and-edit',
  templateUrl: './add-and-edit.component.html',
  styleUrls: ['./add-and-edit.component.css']
})
export class AddAndEditComponent implements OnInit {
  type: string;
  action: string;
  itemGroup: FormGroup;
  id: string;
  categoryOptions: {value: string, name: string}[] = [];
  token: string;
  category: Category;

  constructor(private fb: FormBuilder, private route: ActivatedRoute, private router: Router, private itemService: ItemsService) { }

  ngOnInit(): void {
    this.getType();
    this.getAction();
    this.getId();

    this.token = localStorage.getItem('auth_token');

    this.populateCategoryOptions();
    this.createForm();

  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
  }

  private getType(): void {
    this.route.paramMap.subscribe(params => {
      const type = params.get('type');
      if (type === 'item') {
        this.type = 'item';
      } else if (type === 'category') {
        this.type = 'category';
      } else {
        this.router.navigateByUrl('/admin');
      }
    });
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

  AddEdit(): void {
    if (this.itemGroup.invalid) {
      return;
    }
    if (this.action === 'edit') {
      console.log('EDITING FILE');
    } else {
      console.log('ADDING FILE');

      const item = new Item();
      item.name = this.itemGroup.value.name;
      item.description = this.itemGroup.value.description;
      item.specifications = this.itemGroup.value.specifications;
      item.price = this.itemGroup.value.price;
      item.sellMoney = this.itemGroup.value.sellMoney;
      item.brand = this.itemGroup.value.brand;
      item.quantity = this.itemGroup.value.quantity;
      item.category = this.itemGroup.value.category;
      item.discount = this.itemGroup.value.discount;
      item.picture = this.itemGroup.value.picture;
      console.log(item);
    }
  }

  private populateCategoryOptions(): void {
    this.itemService.getCategories().subscribe(response => {
      for (const category of response) {
        this.categoryOptions.push({value: category.id.toString(), name: category.name});
      }
    });
  }

  private createForm(): void {
    if (this.type === 'item') {
      this.itemGroup = this.fb.group({
        name: new FormControl('', Validators.required),
        description: new FormControl('', Validators.required),
        specification: new FormControl('', Validators.required),
        price: new FormControl('', [Validators.required, Validators.min(1)]),
        sellMoney: new FormControl('', [Validators.required, Validators.min(1)]),
        brand: new FormControl('', Validators.required),
        quantity: new FormControl('', [Validators.required, Validators.min(1)]),
        category: new FormControl(null, Validators.required),
        discount: new FormControl('', [Validators.required, Validators.min(1)]),
        picture: new FormControl('', Validators.required),
      });
    } else {
      this.itemGroup = this.fb.group({
        name: new FormControl('', Validators.required)
      });
    }
  }

  addCategory(): void {
    if (this.itemGroup.invalid) {
      return;
    }

    const name = this.itemGroup.value.name;
    this.itemService.addCategory(this.token, name).subscribe(response => {
      console.log(response);
    });

  }

  editCategory(): void {
    if (this.itemGroup.invalid) {
      return;
    }

    this.itemService.getCategories().subscribe(resposne => {

    })
  }
}
