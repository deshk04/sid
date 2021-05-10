import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulelogComponent } from './schedulelog.component';

describe('SchedulelogComponent', () => {
  let component: SchedulelogComponent;
  let fixture: ComponentFixture<SchedulelogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SchedulelogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SchedulelogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
