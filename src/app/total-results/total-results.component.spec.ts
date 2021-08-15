import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalResultsComponent } from './total-results.component';

describe('TotalResultsComponent', () => {
  let component: TotalResultsComponent;
  let fixture: ComponentFixture<TotalResultsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalResultsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TotalResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
