import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApprovePurchasesComponent } from './approve-purchases.component';

describe('ApprovePurchasesComponent', () => {
  let component: ApprovePurchasesComponent;
  let fixture: ComponentFixture<ApprovePurchasesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ApprovePurchasesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ApprovePurchasesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
