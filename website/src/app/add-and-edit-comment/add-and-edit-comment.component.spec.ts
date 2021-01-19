import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddAndEditCommentComponent } from './add-and-edit-comment.component';

describe('AddAndEditCommentComponent', () => {
  let component: AddAndEditCommentComponent;
  let fixture: ComponentFixture<AddAndEditCommentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddAndEditCommentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddAndEditCommentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
