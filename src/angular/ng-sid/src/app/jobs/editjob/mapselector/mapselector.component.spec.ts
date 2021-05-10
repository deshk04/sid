import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MapselectorComponent } from './mapselector.component';

describe('MapselectorComponent', () => {
  let component: MapselectorComponent;
  let fixture: ComponentFixture<MapselectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MapselectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MapselectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
