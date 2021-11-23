import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FullStatisticsListComponent } from './full-statistics-list.component';

describe('FullStatisticsListComponent', () => {
  let component: FullStatisticsListComponent;
  let fixture: ComponentFixture<FullStatisticsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FullStatisticsListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FullStatisticsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
