import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditscheduleComponent } from './editschedule.component';

describe('EditscheduleComponent', () => {
  let component: EditscheduleComponent;
  let fixture: ComponentFixture<EditscheduleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditscheduleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditscheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
