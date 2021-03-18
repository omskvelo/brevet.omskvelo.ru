import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {now} from 'moment';
import {MatDialog} from '@angular/material/dialog';
import {HttpClient} from '@angular/common/http';

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
  brevetsData: BrevetsData[];
  routesData: RoutesData[];

  constructor(private dialog: MatDialog, private httpClient: HttpClient) {
    this.httpClient.get('assets/brevetsData.json')
      .subscribe((data: BrevetsData[]) => this.brevetsData = data);
    this.httpClient.get('assets/routesData.json')
      .subscribe((data: RoutesData[]) => this.routesData = data);
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
  }

  ngOnInit(): void {
  }

  dialogShowRoute(brevet, routes): void {
    this.dialog.open(DialogShowRouteComponent, {
      data: {brevet, routes}
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
