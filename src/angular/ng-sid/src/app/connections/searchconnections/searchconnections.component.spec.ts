import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchConnectionsComponent } from './searchconnections.component';

describe('SearchConnectionsComponent', () => {
  let component: SearchConnectionsComponent;
  let fixture: ComponentFixture<SearchConnectionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchConnectionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchConnectionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
