import { TestBed } from '@angular/core/testing';

import { PropertiesResolver } from './properties.resolver';

describe('PropertiesResolver', () => {
  let resolver: PropertiesResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(PropertiesResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
