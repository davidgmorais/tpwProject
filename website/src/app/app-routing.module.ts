import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule, Routes} from '@angular/router';
import {HomepageComponent} from './homepage/homepage.component';
import {SearchResultsComponent} from './items/search-results/search-results.component';
import {ItemListComponent} from './items/item-list/item-list.component';
import {LoginComponent} from './account/login/login.component';
import {RegisterComponent} from './account/register/register.component';
import {ItemPageComponent} from './items/item-page/item-page.component';
import {DashboardComponent} from './admin/dashboard/dashboard.component';
import {ManagementTableComponent} from './admin/management-table/management-table.component';
import {AddAndEditComponent} from './admin/add-and-edit/add-and-edit.component';
import {AddEditCategoryComponent} from './admin/add-edit-category/add-edit-category.component';
import {AddEditSubcategoryComponent} from './admin/add-edit-subcategory/add-edit-subcategory.component';
import {OutOfStockComponent} from './admin/out-of-stock/out-of-stock.component';
import {ApprovePurchasesComponent} from './admin/approve-purchases/approve-purchases.component';
import {PurchaseDetailsComponent} from './admin/purchase-details/purchase-details.component';
import { ProfileComponent } from './profile/profile.component';
import { AddAndEditCommentComponent } from './add-and-edit-comment/add-and-edit-comment.component';
import { CartComponent } from './cart/cart.component';

const routes: Routes = [
  {path: '', component: HomepageComponent},
  {path: 'search', component: SearchResultsComponent},
  {path: 'items', component: ItemListComponent},
  {path: 'items/:id', component: ItemListComponent},
  {path: 'items/:id/:slug', component: ItemListComponent},
  {path: 'item/:id', component: ItemPageComponent},

  {path: 'login', component: LoginComponent},
  {path: 'registration', component: RegisterComponent},

  {path: 'admin', component: DashboardComponent},
  {path: 'admin/outofstock', component: OutOfStockComponent},
  {path: 'admin/outofstock/:id', component: OutOfStockComponent},
  {path: 'admin/purchases', component: ApprovePurchasesComponent},
  {path: 'admin/purchases/:id', component: PurchaseDetailsComponent},
  {path: 'admin/:type', component: ManagementTableComponent},
  {path: 'admin/item/:action/:id', component: AddAndEditComponent},
  {path: 'admin/item/:action', component: AddAndEditComponent},
  {path: 'admin/category/:action/:id', component: AddEditCategoryComponent},
  {path: 'admin/category/:action', component: AddEditCategoryComponent},
  {path: 'admin/subcategory/:action/:id', component: AddEditSubcategoryComponent},
  {path: 'admin/subcategory/:action', component: AddEditSubcategoryComponent},

  {path: 'cart', component: CartComponent},

  {path: 'account', component: ProfileComponent},
  {path: 'account/comments/:action', component: AddAndEditCommentComponent},
  {path: 'account/comments/:action/:id', component: AddAndEditCommentComponent},

  {path: '**', redirectTo: ''}
];

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    RouterModule.forRoot(routes, {scrollPositionRestoration: 'enabled'})
  ],
  exports: [
    RouterModule
  ]
})
export class AppRoutingModule { }
