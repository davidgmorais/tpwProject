import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {Profile} from '../../models/Profile';
import { User } from '../../models/User';
import {ActivatedRoute, Router} from '@angular/router';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerGroup: FormGroup;
  raiseErrors: boolean;
  profile: Profile;
  token: string;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService
  ) { }

  ngOnInit(): void {
    this.registerGroup = this.fb.group({
      username: ['', Validators.required],
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', Validators.required],
      birthdate: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  register(): void {
    alert('register');
    if (this.registerGroup.invalid) {
      this.raiseErrors = true;
      return;
    }
    this.raiseErrors = false;
    const user = new User();
    user.username = this.registerGroup.value.username;
    user.email = this.registerGroup.value.email;
    user.password = this.registerGroup.value.password;

    const profile = new Profile();
    profile.user = user;
    profile.firstName = this.registerGroup.value.firstName;
    profile.lastName = this.registerGroup.value.lastName;
    profile.money = 0;
    profile.birthdate = this.registerGroup.value.birthdate;

    this.userService.register(profile).subscribe(response => {
      this.router.navigateByUrl('/');
    });

    this.userService.login(user.username, user.password).subscribe(response => {
      this.token = response.token;
      localStorage.setItem('auth_token', this.token);
      localStorage.setItem('username', user.username);
      this.router.navigateByUrl('/');
    });
  }
}
