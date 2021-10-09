import {TestBed} from '@angular/core/testing';

import {RoutesResolver} from './routes.resolver';

describe('RoutersResolver', () => {
  let resolver: RoutesResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(RoutesResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
