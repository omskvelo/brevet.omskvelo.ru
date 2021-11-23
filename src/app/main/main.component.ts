import {Component, OnInit} from '@angular/core';
import {now} from 'moment';
import {MatDialog} from '@angular/material/dialog';
import {ActivatedRoute, Router} from '@angular/router';
import {DatePipe} from '@angular/common';
import {BrevetsData, ResultsData} from '../shell/shell.component';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
})
export class MainComponent implements OnInit {
  brevetsData: BrevetsData[];
  resultsData: ResultsData[];
  nowDate = new Date(now()).getTime();
  startDate: number;
  finishDate: number;
  years = [];
  colors = [];
  yearNow = this.datePipe.transform(new Date(now()), 'yyyy');
  year: string;
  emptyBrevetsData = false;

  constructor(private dialog: MatDialog,
              private router: Router,
              private activatedRoute: ActivatedRoute,
              private datePipe: DatePipe) {
  }

  ngOnInit(): void {
    this.activatedRoute.paramMap
      .subscribe(data => {
        this.year = data.get('year');
        if (this.year === null || this.activatedRoute.snapshot.data.propertiesResolver.years.filter(x => x === this.year).length === 0) {
          this.router.navigate([this.yearNow]).then();
        } else {
          this.years = this.activatedRoute.snapshot.data.propertiesResolver.years;
          this.colors = this.activatedRoute.snapshot.data.propertiesResolver.colors;
          this.resultsData = this.activatedRoute.snapshot.data.resultsResolver;
          this.loadCalendar();
        }
      });
  }

  selectYear(year): void {
    this.router.navigate([year]).then();
    this.loadCalendar();
  }

  loadCalendar(): void {
    this.activatedRoute.data
      .subscribe(data => {
          this.brevetsData = data.brevetsResolver;
          this.emptyBrevetsData = this.brevetsData.length === 0;
          for (const item of this.brevetsData) {
            const splitDate = item.startDate.split('.');
            const splitTime = item.startTime.split('.');
            const totalTime = [Math.trunc(item.totalTime), (item.totalTime - Math.trunc(item.totalTime)) * 60];
            this.startDate = new Date(
              +splitDate[2],
              +splitDate[1] - 1,
              +splitDate[0],
              +splitTime[0],
              +splitTime[1]
            ).getTime();
            this.finishDate = new Date(
              +splitDate[2],
              +splitDate[1] - 1,
              +splitDate[0],
              +splitTime[0] + totalTime[0],
              +splitTime[1] + totalTime[1]
            ).getTime();
            if (this.startDate > this.nowDate) {
              item.status =
                'Начало заезда: ' + this.datePipe.transform(new Date(this.startDate), 'dd.MM.yyyy, HH.mm') + ', ' +
                'лимит ' + item.totalTime + 'ч.';
            }
            if (this.startDate < this.nowDate && this.finishDate > this.nowDate) {
              item.status =
                'Заезд начался. Окончание: ' + this.datePipe.transform(new Date(this.finishDate), 'dd.MM.yyyy, HH.mm') + ', ' +
                'лимит ' + item.totalTime + 'ч.';
            }
            if (this.startDate < this.nowDate && this.finishDate < this.nowDate) {
              item.status = 'Заезд завершен.';
            }
          }
        },
        _ => {
          this.emptyBrevetsData = true;
        });
  }

  dialogShowResult(route, index, distance): void {
    for (const item of this.resultsData) {
      if (item.title === route && item.index === index) {
        this.dialog.open(DialogShowResultComponent, {
          data: {results: item.results, distance}
        });
        break;
      }
    }
  }

  showRoute(year, routeTitle): void {
    this.router.navigate([year + '/' + routeTitle]).then();
  }

  showTotalResults(year): void {
    this.router.navigate([year + '/total_results']).then();
  }

  showStatistics(year): void {
    this.router.navigate([year + '/statistics']).then();
  }
}

@Component({
  selector: 'app-dialog-show-result',
  templateUrl: './dialog-show-result.component.html',
  styleUrls: ['./main.component.css'],
})
export class DialogShowResultComponent {
  constructor() {
  }
}
