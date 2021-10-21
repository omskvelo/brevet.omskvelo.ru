import {Component, OnInit} from '@angular/core';

export interface BrevetsData {
  route: string;
  index: number;
  title: string;
  startDate: string;
  startTime: string;
  totalTime: number;
  distance: number;
  description: string;
  status: string;
}

export interface RoutesData {
  title: string;
  checkPoints: any;
  wayPoints: any;
}

export interface ResultsData {
  title: string;
  index: number;
  results: any;
}

@Component({
  selector: 'app-shell',
  templateUrl: './shell.component.html',
  styleUrls: ['./shell.component.css']
})
export class ShellComponent implements OnInit {
  constructor() {
  }

  ngOnInit(): void {
  }
}
