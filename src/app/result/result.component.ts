import {AfterViewInit, Component, Inject, ViewChild} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements AfterViewInit {
  displayedColumns: string[] = ['name', 'resultTime'];
  results = new MatTableDataSource(this.data.results);
  amount = this.data.results.length;
  resultsTable = true;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data) {
  }

  ngAfterViewInit(): void {
    this.resultsTable = this.data.results.length !== 0;
    this.results.sort = this.sort;
  }

  dialogClose(): void {
    this.dialog.closeAll();
  }
}
