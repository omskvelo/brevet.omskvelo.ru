import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {take} from 'rxjs/operators';
import {BrevetsData, ResultsData} from '../main/main.component';

@Component({
  selector: 'app-total-results',
  templateUrl: './total-results.component.html',
  styleUrls: ['./total-results.component.css']
})
export class TotalResultsComponent implements OnInit {
  displayedColumns = ['participant'];
  brevetsData: BrevetsData[];
  jsonData: ResultsData[];
  name = [];
  total = [];
  amount: number;
  year: string;

  constructor(private activatedRoute: ActivatedRoute, private router: Router) {
  }

  ngOnInit(): void {
    this.activatedRoute.paramMap.pipe(take(1))
      .subscribe(data => this.year = data.get('year'));
    this.brevetsData = this.activatedRoute.snapshot.data.brevetsResolver;
    this.jsonData = this.activatedRoute.snapshot.data.resultsResolver;
    for (const item of this.brevetsData) {
      this.displayedColumns.push(item.route + item.index);
    }
    this.displayedColumns.push('inAll', 'sr');
    let i = 0;
    let j = 0;
    for (const jsonDataItem of this.jsonData) {
      for (const resultsItem of jsonDataItem.results) {
        j = 0;
        for (const item of this.name) {
          if (item === resultsItem.name) {
            j = 1;
            break;
          }
        }
        if (j === 0) {
          this.name[i] = resultsItem.name;
          i++;
          j = 0;
        }
      }
    }
    this.name = this.name.sort();
    i = 0;
    for (const item of this.name) {
      this.total[i] = [item];
      for (j = 1; j <= this.jsonData.length + 2; j++) {
        this.total[i][j] = '-';
      }
      i++;
    }
    i = 0;
    j = 1;
    for (const jsonDataItem of this.jsonData) {
      for (const resultsItem of jsonDataItem.results) {
        i = 0;
        for (const item of this.total) {
          if (item[0] === resultsItem.name) {
            this.total[i][j] = resultsItem.resultTime;
          }
          i++;
        }
      }
      j++;
    }
    let totalKM = 0;
    let SR = [0, 0, 0, 0];
    for (const item of this.total) {
      totalKM = 0;
      SR = [0, 0, 0, 0];
      for (j = 1; j < item.length; j++) {
        if (item[j] !== '-' && item[j] !== 'DNS' && item[j] !== 'DNF' && item[j] !== 'DNQ' && item[j] !== 'OTL') {
          totalKM = totalKM + this.brevetsData[j - 1].distance;
          switch (this.brevetsData[j - 1].distance) {
            case 200: {
              SR[0] = 1;
              break;
            }
            case 300: {
              SR[1] = 1;
              break;
            }
            case 400: {
              SR[2] = 1;
              break;
            }
            case 600: {
              SR[3] = 1;
              break;
            }
          }
        }
      }
      item[this.jsonData.length + 1] = totalKM;
      if (SR[0] === 1 && SR[1] === 1 && SR[2] === 1 && SR[3] === 1) {
        item[this.jsonData.length + 2] = 'СР';
      }
    }
    this.amount = this.total.length;
  }

  dialogClose(year): void {
    this.router.navigate([year]).then();
  }
}
