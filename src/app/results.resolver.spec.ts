import { TestBed } from '@angular/core/testing';

import { ResultsResolver } from './results.resolver';

describe('ResultsResolver', () => {
  let resolver: ResultsResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(ResultsResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
