import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Awss3Component } from './awss3.component';

describe('Awss3Component', () => {
  let component: Awss3Component;
  let fixture: ComponentFixture<Awss3Component>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Awss3Component ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Awss3Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
