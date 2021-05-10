import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SourceselectorComponent } from './sourceselector.component';

describe('SourceselectorComponent', () => {
  let component: SourceselectorComponent;
  let fixture: ComponentFixture<SourceselectorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SourceselectorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SourceselectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
