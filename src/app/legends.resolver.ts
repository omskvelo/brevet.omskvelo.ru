import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Observable, of} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LegendsResolver implements Resolve<any> {
  constructor(private http: HttpClient) {
  }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<any> {
    const year = route.paramMap.get('year');
    const routeTitle = route.paramMap.get('routeTitle');
    return this.http.get('assets/' + year + '/legends/' + routeTitle + '.json').pipe(catchError(_ => {
      return of([]);
    }));
  }
}
