import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DestselectorComponent } from './destselector.component';

describe('DestselectorComponent', () => {
  let component: DestselectorComponent;
  let fixture: ComponentFixture<DestselectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DestselectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DestselectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
