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
  {path: 'admin/:type', component: ManagementTableComponent},
  {path: 'admin/:type/:action/:id', component: AddAndEditComponent},
  {path: 'admin/:type/:action', component: AddAndEditComponent},

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
