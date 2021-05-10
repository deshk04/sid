import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JoblogdetailsComponent } from './joblogdetails.component';

describe('JoblogdetailsComponent', () => {
  let component: JoblogdetailsComponent;
  let fixture: ComponentFixture<JoblogdetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JoblogdetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JoblogdetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
