import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Comments } from '../models/Comments';
import { Profile } from '../models/Profile';
import { Sell } from '../models/Sell';
import { Purchase } from '../models/Purchase';
import {UserService} from '../services/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  profile: Profile;
  sells: Sell[];
  purchases: Purchase[];
  comments: Comments[] = [];
  token: string;
  profileId: number;

  constructor(private route: ActivatedRoute, private router: Router, private userService: UserService) { }

  ngOnInit(): void {
    this.token = localStorage.getItem('username');
    this.getProfile(this.token);
  }

  private getProfile(token: string): void {
    this.userService.getAccounts().subscribe(response => {
      this.profile = response.filter(i => i.user.username === token)[0];
      this.getComments(this.token);
      this.getPurchases(this.token);
      this.getSells(this.token);
    });
  }

  private getComments(token: string): void {
    this.profileId = this.profile.id;
    this.userService.getComments().subscribe(response => {
      this.comments = response.filter(i => i.user === this.profile.user.id);
    });
  }

 private getPurchases(token: string): void {
    this.profileId = this.profile.id;
    this.userService.getPurchases().subscribe(response => {
      console.log(response);
      this.purchases = response.filter(i => i.user === this.profile.user);
    });
  }

  private getSells(token: string): void {
    this.userService.getSells().subscribe(response => {
      this.sells = response.filter(i => i.user.id === this.profile.user.id);
    });
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('username');
    this.router.navigateByUrl('/');
  }
}
