import { TestBed } from '@angular/core/testing';

import { YearsResolver } from './years.resolver';

describe('YearsResolver', () => {
  let resolver: YearsResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(YearsResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
