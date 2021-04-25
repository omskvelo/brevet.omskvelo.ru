import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {now} from 'moment';
import {MatDialog} from '@angular/material/dialog';
import {HttpClient} from '@angular/common/http';
import {take} from 'rxjs/operators';


export const MY_FORMATS = {
  parse: {
    dateInput: 'DD.MM.YYYY',
  },
  display: {
    dateInput: 'DD.MM.YYYY',
    monthYearLabel: 'DD.MM.YYYY',
    dateA11yLabel: 'DD.MM.YYYY',
    monthYearA11yLabel: 'DD.MM.YYYY'
  }
};

export interface BrevetsData {
  startDate: string;
  startTime: string;
  totalTime: number;
  distance: number;
  title: string;
  color: string;
  route: string;
  description: string;
  status: string;
}

export interface RoutesData {
  title: string;
  checkPoints: any;
  wayPoints: any;
}

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class MainComponent implements OnInit {
  navigationForm = new FormGroup({
    inputDate: new FormControl({value: new Date(now()), disabled: true}),
    allEvents: new FormControl(true)
  });
  optionsDate = {
    hour: 'numeric',
    minute: 'numeric',
    day: 'numeric',
    month: 'numeric',
    year: 'numeric',
  };
  brevetsData: BrevetsData[];
  routesData: RoutesData[];
  nowDate = new Date(now()).getTime();
  startDate;
  finishDate;

  constructor(private dialog: MatDialog, private httpClient: HttpClient) {
  }

  dateClass = date => {
    for (const item of this.brevetsData) {
      let day = date._i.date;
      if (day < 10) {
        day = '0' + day;
      }
      let month = date._i.month + 1;
      if (month < 10) {
        month = '0' + month;
      }
      if (day + '.' + month + '.' + date._i.year === item.startDate) {
        return (date) ? item.color : undefined;
      }
    }
  };

  ngOnInit(): void {
    this.httpClient.get('assets/data/brevetsData.json').pipe(take(1))
      .subscribe((data: BrevetsData[]) => {
        this.brevetsData = data;
        for (const item of this.brevetsData) {
          const splitDate = item.startDate.split('.');
          const splitTime = item.startTime.split('.');
          const totalTime = [Math.trunc(item.totalTime), (item.totalTime - Math.trunc(item.totalTime)) * 60];
          this.startDate = new Date(Number(splitDate[2]), Number(splitDate[1]) - 1, Number(splitDate[0]), Number(splitTime[0]), Number(splitTime[1])).getTime();
          this.finishDate = new Date(Number(splitDate[2]), Number(splitDate[1]) - 1, Number(splitDate[0]), Number(splitTime[0]) + totalTime[0], Number(splitTime[1]) + totalTime[1]).getTime();
          if (this.startDate > this.nowDate) {
            item.status = 'Начало заезда: ' + new Date(this.startDate).toLocaleString('ru', this.optionsDate) + ', лимит ' + item.totalTime + 'ч.';
          }
          if (this.startDate < this.nowDate && this.finishDate > this.nowDate) {
            item.status = 'Заезд начался. Окончание: ' + new Date(this.finishDate).toLocaleString('ru', this.optionsDate) + ', лимит ' + item.totalTime + 'ч.';
          }
          if (this.startDate < this.nowDate && this.finishDate < this.nowDate) {
            item.status = 'Заезд закончился.';
          }
        }
      });
    this.httpClient.get('assets/data/routesData.json').pipe(take(1))
      .subscribe((data: RoutesData[]) => this.routesData = data);
  }

  dialogShowRoute(brevet, routes): void {
    this.dialog.open(DialogShowRouteComponent, {
      data: {brevet, routes}
    });
  }
  dialogShowResult(route): void {
    this.dialog.open(DialogShowResultComponent, {
      data: {route}
    });
  }
}

@Component({
  selector: 'app-dialog-show-route',
  templateUrl: './dialog-show-route.component.html',
  styleUrls: ['./main.component.css'],
})
export class DialogShowRouteComponent {
  constructor() {
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
