import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ActivatedRoute, Router} from '@angular/router';
import {Comments} from '../models/Comments';
import {Item} from '../models/Item';
import {Profile} from '../models/Profile';
import {UserService} from '../services/user.service';

@Component({
  selector: 'app-add-and-edit-comment',
  templateUrl: './add-and-edit-comment.component.html',
  styleUrls: ['./add-and-edit-comment.component.css']
})
export class AddAndEditCommentComponent implements OnInit {
  action: string;
  commentGroup: FormGroup;
  id: string;
  profile: Profile;
  item: Item;
  token: string;
  comment: Comments;
  itemOptions: Item[] = [];

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private userService: UserService,
  ) { }

  ngOnInit(): void {
    this.token = localStorage.getItem('username');

    this.getProfile(this.token);
    this.populateItemOptions();

    this.getAction();
    this.getId();
    this.createCommentForm();
    this.getComment();

  }

  private getProfile(token: string): void {
    this.userService.getAccounts().subscribe(response => {
      this.profile = response.filter(i => i.user.username === token)[0];
    });
  }

  // depois por condiçao dos q ja foram comprados
  private populateItemOptions(): void {
    this.userService.getItems().subscribe(response => {
      for (const item of response) {
        this.itemOptions.push(item);
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
        this.router.navigateByUrl('/account');
      }
    });
  }

  private getId(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('id');
      if (this.action === 'add' && id) {
        this.router.navigateByUrl('/account');
      } else if (this.action === 'edit' && !id) {
        this.router.navigateByUrl('/account');
      } else if (id) {
        this.id = id;
        this.getComment();
      } else {
        this.createCommentForm();
      }
    });
  }

  private createCommentForm(): void {
    if (this.action === 'add') {
      this.commentGroup = this.fb.group({
        text: new FormControl('', Validators.required),
        stars: new FormControl('', [Validators.required, Validators.min(0), Validators.max(5)]),
        item: new FormControl(null, Validators.required),
      });
    } else {
      this.commentGroup = this.fb.group({
        text: new FormControl('', Validators.required),
        stars: new FormControl('', [Validators.required, Validators.min(0), Validators.max(5)]),
      });
    }
  }

  private getComment(): void {
    if (this.id) {
      this.userService.getCommentInfo(+this.id).subscribe(response => {
        this.comment = response;
        if (this.action === 'add') {
          this.commentGroup.patchValue({
            text: this.comment.text,
            stars: this.comment.stars,
            user: this.comment.user,
          });
        } else {
          this.commentGroup.patchValue({
            text: this.comment.text,
            stars: this.comment.stars,
          });
          this.item = this.comment.item;
        }
      });
    }
  }

  addComment(): void {
    if (this.commentGroup.invalid) {
      return;
    }

    const comment = new Comments();

    comment.text = this.commentGroup.value.text;
    comment.stars = this.commentGroup.value.stars;
    comment.item = this.commentGroup.value.item;
    comment.user = this.profile.user.id;
    console.log(this.profile);

    this.userService.addComment(comment).subscribe(response => {
      this.router.navigateByUrl('account');
    });

  }

  editComment(): void {
    if (this.commentGroup.invalid) {
      return;
    }

    this.comment.text = this.commentGroup.value.text;
    this.comment.stars = this.commentGroup.value.stars;

    this.userService.editComment(this.comment).subscribe(response => {
      this.router.navigateByUrl('account');
    });
  }

  deleteComment(): void {
    this.userService.deleteComment(this.comment.id).subscribe(response => {
      this.router.navigateByUrl('/account');
    });
  }
}

