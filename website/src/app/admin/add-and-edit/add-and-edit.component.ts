import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {Category} from '../../models/Category';
import {ItemsService} from '../../services/items.service';
import {Item} from '../../models/Item';
import {DatePipe} from '@angular/common';

@Component({
  selector: 'app-add-and-edit',
  templateUrl: './add-and-edit.component.html',
  styleUrls: ['./add-and-edit.component.css']
})
export class AddAndEditComponent implements OnInit {
  action: string;
  itemGroup: FormGroup;
  id: string;
  categoryOptions: Category[] = [];
  token: string;
  category: Category;
  item: Item;
  raiseErrors: boolean;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private itemService: ItemsService,
    public datepipe: DatePipe
  ) { }

  ngOnInit(): void {
    this.getAction();
    this.getId();

    this.token = localStorage.getItem('auth_token');

    this.populateCategoryOptions();
    this.createItemForm();

  }

  toggleFunction(): void {
    document.getElementById('wrapper').classList.toggle('toggled');
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
      } else if (id) {
        this.id = id;
        this.getItem();
      } else {
        this.createItemForm();
      }
    });
  }

  private populateCategoryOptions(): void {
    this.itemService.getCategories().subscribe(response => {
      for (const category of response) {
        this.categoryOptions.push(category);
      }
    });
  }

  private createItemForm(): void {
    this.itemGroup = this.fb.group({
      name: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      specification: new FormControl('', Validators.required),
      price: new FormControl('', [Validators.required, Validators.min(0.01)]),
      sellMoney: new FormControl('', [Validators.required, Validators.min(0.01)]),
      brand: new FormControl('', Validators.required),
      quantity: new FormControl('', [Validators.required, Validators.min(1)]),
      category: new FormControl(null, Validators.required),
      discount: new FormControl('', [Validators.required, Validators.min(1)]),
      picture: new FormControl('', Validators.required),
      pictureSource: new FormControl('', Validators.required),
    });
  }

  onPictureChange(event): void {
    const reader = new FileReader();

    if (event.target.files && event.target.files.length) {
      const [file] = event.target.files;
      reader.readAsDataURL(file);

      reader.onload = () => {

        this.itemGroup.patchValue({
          pictureSource: reader.result
        });

      };

    }
  }


  private getItem(): void {
    this.itemService.getItemInfo(+this.id).subscribe(response => {
      this.item = response;
      this.itemGroup.patchValue({
        name: this.item.name,
        description: this.item.description,
        specification: this.item.specifications,
        price: this.item.price,
        sellMoney: this.item.sellMoney,
        brand: this.item.brand,
        quantity: this.item.quantity,
        category: this.item.category,
        discount: this.item.discount,
        pictureSource: this.item.picture
      });
    });
  }

  addItem(): void {
    if (this.itemGroup.invalid) {
      this.raiseErrors = true;
      return;
    }

    this.raiseErrors = false;
    const item = new Item();

    item.name = this.itemGroup.value.name;
    item.description = this.itemGroup.value.description;
    item.specifications = this.itemGroup.value.specification;
    item.price = this.itemGroup.value.price;
    item.sellMoney = this.itemGroup.value.sellMoney;
    item.brand = this.itemGroup.value.brand;
    item.quantity = this.itemGroup.value.quantity;
    item.category = this.itemGroup.value.category;
    item.discount = this.itemGroup.value.discount;
    item.picture = this.itemGroup.value.pictureSource;
    item.insertDate = this.datepipe.transform(new Date(), 'yyyy-MM-dd');

    this.itemService.addItem(this.token, item).subscribe(response => {
      this.router.navigateByUrl('/admin/item');
    });
  }

  editItem(): void {
    if (this.itemGroup.invalid) {
      this.raiseErrors = true;
      return;
    }
    this.raiseErrors = false;
    this.item.name = this.itemGroup.value.name;
    this.item.description = this.itemGroup.value.description;
    this.item.specifications = this.itemGroup.value.specification;
    this.item.price = this.itemGroup.value.price;
    this.item.sellMoney = this.itemGroup.value.sellMoney;
    this.item.brand = this.itemGroup.value.brand;
    this.item.quantity = this.itemGroup.value.quantity;
    this.item.category = this.itemGroup.value.category;
    this.item.discount = this.itemGroup.value.discount;

    if (this.itemGroup.controls.picture.touched) {
      this.item.picture = this.itemGroup.value.pictureSource;
    }

    // tá a dar erro a dar upload a imagem !!!
//      this.item.picture = null;

    this.itemService.upgradeItem(this.token, this.item).subscribe(response => {
      this.router.navigateByUrl('/admin/item');
    });

  }

  deleteItem(): void {
    this.itemService.deleteItem(this.token, this.item.id).subscribe(response => {
      this.router.navigateByUrl('/admin/item');
    });
  }
}

