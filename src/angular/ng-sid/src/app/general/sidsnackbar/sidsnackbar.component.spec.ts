import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SidSnackbarComponent } from './sidsnackbar.component';

describe('SidSnackbarComponent', () => {
  let component: SidSnackbarComponent;
  let fixture: ComponentFixture<SidSnackbarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SidSnackbarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SidSnackbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
