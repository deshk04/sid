import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulelistComponent } from './schedulelist.component';

describe('SchedulelistComponent', () => {
  let component: SchedulelistComponent;
  let fixture: ComponentFixture<SchedulelistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SchedulelistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SchedulelistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
