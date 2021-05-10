import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SalesforcequeryComponent } from './salesforcequery.component';

describe('SalesforcequeryComponent', () => {
  let component: SalesforcequeryComponent;
  let fixture: ComponentFixture<SalesforcequeryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SalesforcequeryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SalesforcequeryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
