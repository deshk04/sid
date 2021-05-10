import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { JoblogsComponent } from './joblogs.component';

describe('JoblogsComponent', () => {
  let component: JoblogsComponent;
  let fixture: ComponentFixture<JoblogsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ JoblogsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(JoblogsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
