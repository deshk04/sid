import { TestBed } from '@angular/core/testing';

import { JoblogsService } from './joblogs.service';

describe('JoblogsService', () => {
  let service: JoblogsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(JoblogsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
