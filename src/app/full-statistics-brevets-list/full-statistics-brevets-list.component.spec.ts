import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FullStatisticsBrevetsListComponent } from './full-statistics-brevets-list.component';

describe('FullStatisticsBrevetsListComponent', () => {
  let component: FullStatisticsBrevetsListComponent;
  let fixture: ComponentFixture<FullStatisticsBrevetsListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FullStatisticsBrevetsListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FullStatisticsBrevetsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
