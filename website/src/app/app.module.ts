import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { HomepageComponent } from './homepage/homepage.component';
import { NavbarComponent } from './navbar/navbar.component';
import {ReactiveFormsModule} from '@angular/forms';
import { SearchResultsComponent } from './items/search-results/search-results.component';
import { ItemListComponent } from './items/item-list/item-list.component';
import { LoginComponent } from './account/login/login.component';
import { RegisterComponent } from './account/register/register.component';
import { ItemPageComponent } from './items/item-page/item-page.component';
import {UserService} from './services/user.service';
import {ItemsService} from './services/items.service';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { ManagementTableComponent } from './admin/management-table/management-table.component';
import { AddAndEditComponent } from './admin/add-and-edit/add-and-edit.component';
import { AddEditCategoryComponent } from './admin/add-edit-category/add-edit-category.component';
import { AddEditSubcategoryComponent } from './admin/add-edit-subcategory/add-edit-subcategory.component';
import {DatePipe} from '@angular/common';
import { OutOfStockComponent } from './admin/out-of-stock/out-of-stock.component';
import { ApprovePurchasesComponent } from './admin/approve-purchases/approve-purchases.component';
import { PurchaseDetailsComponent } from './admin/purchase-details/purchase-details.component';
import { ProfileComponent } from './profile/profile.component';
import { AddAndEditCommentComponent } from './add-and-edit-comment/add-and-edit-comment.component';

@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    NavbarComponent,
    SearchResultsComponent,
    ItemListComponent,
    LoginComponent,
    RegisterComponent,
    ItemPageComponent,
    DashboardComponent,
    ManagementTableComponent,
    AddAndEditComponent,
    AddEditCategoryComponent,
    AddEditSubcategoryComponent,
    OutOfStockComponent,
    ApprovePurchasesComponent,
    PurchaseDetailsComponent,
    ProfileComponent,
    AddAndEditCommentComponent,
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        ReactiveFormsModule
    ],
  providers: [
    UserService,
    ItemsService,
    DatePipe
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
