import { TestBed } from '@angular/core/testing';

import { LegendsResolver } from './legends.resolver';

describe('LegendsResolver', () => {
  let resolver: LegendsResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(LegendsResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
