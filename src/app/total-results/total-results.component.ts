import {Component, OnInit} from '@angular/core';
import {take} from 'rxjs/operators';
import {JsonData} from '../result/result.component';
import {HttpClient} from '@angular/common/http';
import {BrevetsData} from '../main/main.component';
import {MatDialog} from '@angular/material/dialog';

@Component({
  selector: 'app-total-results',
  templateUrl: './total-results.component.html',
  styleUrls: ['./total-results.component.css']
})
export class TotalResultsComponent implements OnInit {
  brevetsData;
  jsonData;
  name = [];
  total = [];

  constructor(private httpClient: HttpClient, private dialog: MatDialog) {
  }

  ngOnInit(): void {
    document.getElementById('total').style.height = (window.innerHeight - 64).toString() + 'px';
    this.httpClient.get('assets/data/brevetsData.json').pipe(take(1)).subscribe((data: BrevetsData) => {
      this.brevetsData = data;
    });
    this.httpClient.get('assets/data/resultsData.json').pipe(take(1)).subscribe((data: JsonData) => {
      this.jsonData = data;
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
    });
  }
  dialogClose(): any {
    this.dialog.closeAll();
  }
}
