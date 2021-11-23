import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';

@Component({
  selector: 'app-full-statistics-list',
  templateUrl: './full-statistics-list.component.html',
  styleUrls: ['./full-statistics-list.component.css']
})
export class FullStatisticsListComponent implements OnInit {
  displayedColumnsStatistics = ['num', 'name', 'brevet200', 'brevet300', 'brevet400', 'brevet600', 'brevet1000', 'successfulBrevets', 'unsuccessfulBrevets', 'totalDistance', 'totalTime', 'SR', 'rating'];
  statisticsData = this.data.statistics;

  constructor(private dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data) {
  }

  ngOnInit(): void {
  }

  dialogClose(): void {
    this.dialog.closeAll();
  }
}
