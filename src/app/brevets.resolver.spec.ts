import { TestBed } from '@angular/core/testing';

import { BrevetsResolver } from './brevets.resolver';

describe('BrevetsResolver', () => {
  let resolver: BrevetsResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(BrevetsResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
