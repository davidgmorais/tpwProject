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
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        ReactiveFormsModule
    ],
  providers: [
    UserService,
    ItemsService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
