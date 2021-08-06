import {Component, Inject, OnInit, ViewChild} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';
import {HttpClient} from '@angular/common/http';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {take} from 'rxjs/operators';

export interface JsonData {
  title: string;
  index: number;
  results: any;
}

export interface ResultsData {
  name: string;
  resultTime: string;
}

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  displayedColumns: string[] = ['name', 'resultTime'];
  resultsData: MatTableDataSource<ResultsData>;
  jsonData;
  amount;
  resultsTable = true;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data, private httpClient: HttpClient) {
  }

  ngOnInit(): void {
    this.httpClient.get('assets/data/resultsData.json').pipe(take(1)).subscribe((data: JsonData) => {
      this.jsonData = data;
      for (const item of this.jsonData) {
        if (item.title === this.data.route && item.index === this.data.index) {
          if (item.results.length === 0) {
            this.resultsTable = false;
          }
          this.resultsData = new MatTableDataSource(item.results);
          this.resultsData.sort = this.sort;
          this.amount = item.results.length;
        }
      }
    });
  }

  dialogClose(): any {
    this.dialog.closeAll();
  }
}
