import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulerecordComponent } from './schedulerecord.component';

describe('SchedulerecordComponent', () => {
  let component: SchedulerecordComponent;
  let fixture: ComponentFixture<SchedulerecordComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SchedulerecordComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SchedulerecordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
