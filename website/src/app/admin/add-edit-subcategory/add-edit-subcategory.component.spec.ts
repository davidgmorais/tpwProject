import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddEditSubcategoryComponent } from './add-edit-subcategory.component';

describe('AddEditSubcategoryComponent', () => {
  let component: AddEditSubcategoryComponent;
  let fixture: ComponentFixture<AddEditSubcategoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddEditSubcategoryComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddEditSubcategoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
