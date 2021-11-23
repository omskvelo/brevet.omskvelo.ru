import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialog} from '@angular/material/dialog';

@Component({
  selector: 'app-full-statistics-brevets-list',
  templateUrl: './full-statistics-brevets-list.component.html',
  styleUrls: ['./full-statistics-brevets-list.component.css']
})
export class FullStatisticsBrevetsListComponent implements OnInit {
  displayedColumns = ['num', 'name', 'resultTime', 'route'];

  constructor(private dialog: MatDialog, @Inject(MAT_DIALOG_DATA) public data) {
  }

  ngOnInit(): void {
  }

  dialogClose(): void {
    this.dialog.closeAll();
  }
}
