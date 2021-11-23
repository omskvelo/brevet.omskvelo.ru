import {Component, OnInit} from '@angular/core';
import {BrevetsData, ResultsData} from '../shell/shell.component';
import {ActivatedRoute, Router} from '@angular/router';
import {take} from 'rxjs/operators';
import {MatDialog} from '@angular/material/dialog';

export interface LeaderboardBrevet {
  number: number;
  name: string;
  resultTime: number;
  route: string;
  startDate: string;
}

export interface StatisticsData {
  number: number;
  name: string;
  brevet200: DistanceData;
  brevet300: DistanceData;
  brevet400: DistanceData;
  brevet600: DistanceData;
  brevet1000: DistanceData;
  successfulBrevets: number;
  unsuccessfulBrevets: number;
  totalDistance: number;
  totalTime: number;
  SR: any;
  rating: number;
}

export interface DistanceData {
  resultTime: number;
  title: string;
  startDate: string;
}

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css']
})
export class StatisticsComponent implements OnInit {
  displayedColumns = ['num', 'name', 'resultTime', 'route'];
  displayedColumnsStatistics = ['num', 'name', 'brevet200', 'brevet300', 'brevet400', 'brevet600', 'brevet1000', 'successfulBrevets', 'unsuccessfulBrevets', 'totalDistance', 'totalTime', 'SR', 'rating'];
  brevetsData: BrevetsData[];
  resultsData: ResultsData[];
  commonArray = [];
  statisticsData: StatisticsData[] = [];
  statisticsDataShort: StatisticsData[] = [];
  colors = [];
  year: string;
  totalDistance = 0;
  totalTime = 0;
  totalParticipants = 0;
  totalSR = 0;
  successfulBrevets = 0;
  unsuccessfulBrevets = 0;
  endingBrevets = '';
  brevet200: LeaderboardBrevet[] = [];
  brevet300: LeaderboardBrevet[] = [];
  brevet400: LeaderboardBrevet[] = [];
  brevet600: LeaderboardBrevet[] = [];
  brevet1000: LeaderboardBrevet[] = [];
  brevet200Short: LeaderboardBrevet[] = [];
  brevet300Short: LeaderboardBrevet[] = [];
  brevet400Short: LeaderboardBrevet[] = [];
  brevet600Short: LeaderboardBrevet[] = [];
  brevet1000Short: LeaderboardBrevet[] = [];

  constructor(private activatedRoute: ActivatedRoute, private router: Router, private dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.activatedRoute.paramMap.pipe(take(1))
      .subscribe(data => this.year = data.get('year'));
    this.brevetsData = this.activatedRoute.snapshot.data.brevetsResolver;
    this.resultsData = this.activatedRoute.snapshot.data.resultsResolver;
    this.colors = this.activatedRoute.snapshot.data.propertiesResolver.colors;
    let i = 0;
    let j = 0;
    let participant;
    let timeArray;
    for (const brevet of this.brevetsData) {
      this.commonArray.push(brevet);
      this.commonArray[i].results = this.resultsData.find(x => x.title === brevet.route && x.index === brevet.index).results;
      for (const result of this.commonArray[i].results) {
        if (!this.statisticsData.find(x => x.name === result.name)) {
          const arrayString: StatisticsData = {
            number: 0,
            name: '',
            brevet200: {resultTime: 0, title: '', startDate: ''},
            brevet300: {resultTime: 0, title: '', startDate: ''},
            brevet400: {resultTime: 0, title: '', startDate: ''},
            brevet600: {resultTime: 0, title: '', startDate: ''},
            brevet1000: {resultTime: 0, title: '', startDate: ''},
            successfulBrevets: 0,
            unsuccessfulBrevets: 0,
            totalDistance: 0,
            totalTime: 0,
            SR: [0, 0, 0, 0],
            rating: 0
          };
          this.statisticsData.push(arrayString);
          this.statisticsData[j].name = result.name;
          j++;
        }
        if (result.resultTime !== 'DNS' &&
          result.resultTime !== 'DNF' &&
          result.resultTime !== 'OTL' &&
          result.resultTime !== 'DSQ') {
          participant = this.statisticsData.find(x => x.name === result.name);
          this.statistics(participant.brevet200, brevet, result, 200);
          this.statistics(participant.brevet300, brevet, result, 300);
          this.statistics(participant.brevet400, brevet, result, 400);
          this.statistics(participant.brevet600, brevet, result, 600);
          this.statistics(participant.brevet1000, brevet, result, 1000);
          participant.totalDistance = participant.totalDistance + brevet.distance;
          const timeArrayResult = result.resultTime.split('.');
          const totalTime = +timeArrayResult[0] + +(timeArrayResult[1] / 60) +
            Math.floor(participant.totalTime) + ((participant.totalTime - Math.floor(participant.totalTime)) / 60);
          participant.totalTime = Math.floor(totalTime) + ((totalTime - Math.floor(totalTime)) * 60) / 100;
          participant.successfulBrevets++;
          this.totalDistance = this.totalDistance + brevet.distance;
          timeArray = result.resultTime.split('.');
          this.totalTime = this.totalTime + +timeArray[0] + +(timeArray[1] / 60);
          this.successfulBrevets++;
          this.distanceBrevet(this.brevet200, brevet, result, 200);
          this.distanceBrevet(this.brevet300, brevet, result, 300);
          this.distanceBrevet(this.brevet400, brevet, result, 400);
          this.distanceBrevet(this.brevet600, brevet, result, 600);
          this.distanceBrevet(this.brevet1000, brevet, result, 1000);
          switch (brevet.distance) {
            case 200: {
              participant.SR[0]++;
              break;
            }
            case 300: {
              participant.SR[1]++;
              break;
            }
            case 400: {
              participant.SR[2]++;
              break;
            }
            case 600: {
              participant.SR[3]++;
              break;
            }
          }
        } else {
          this.unsuccessfulBrevets++;
          participant = this.statisticsData.find(x => x.name === result.name);
          participant.unsuccessfulBrevets++;
        }
      }
      i++;
    }
    this.totalTime = Math.floor(this.totalTime);
    this.totalParticipants = this.statisticsData.length;
    this.endingBrevets = this.endingWord(this.successfulBrevets + this.unsuccessfulBrevets);
    this.sortAndShort(this.brevet200, this.brevet200Short);
    this.sortAndShort(this.brevet300, this.brevet300Short);
    this.sortAndShort(this.brevet400, this.brevet400Short);
    this.sortAndShort(this.brevet600, this.brevet600Short);
    this.sortAndShort(this.brevet1000, this.brevet1000Short);
    this.endingWord(this.statisticsData.length);
    for (const statistic of this.statisticsData) {
      statistic.SR = this.SR(statistic.SR);
      if (statistic.SR !== 0) {
        this.totalSR++;
      }
      const multiplierLeaderboard =
        this.multiplierLeaderboard(this.brevet200, statistic.name) +
        this.multiplierLeaderboard(this.brevet300, statistic.name) +
        this.multiplierLeaderboard(this.brevet400, statistic.name) +
        this.multiplierLeaderboard(this.brevet600, statistic.name) +
        this.multiplierLeaderboard(this.brevet1000, statistic.name);
      let multiplier = 1 + multiplierLeaderboard;
      if (statistic.SR > 0) {
        multiplier = multiplier + statistic.SR * 0.5;
      }
      statistic.rating = statistic.totalDistance * multiplier *
        (statistic.successfulBrevets / (statistic.successfulBrevets + statistic.unsuccessfulBrevets));
    }
    this.statisticsData.sort((a, b) => b.rating - a.rating || a.name.localeCompare(b.name));
    let rating = 0;
    i = 0;
    for (const statistic of this.statisticsData) {
      if (statistic.rating !== rating) {
        rating = statistic.rating;
        i++;
      }
      statistic.number = i;
      statistic.rating = Math.floor(statistic.rating);
      if (i < 6) {
        this.statisticsDataShort.push(statistic);
      }
    }
  }

  distanceBrevet(leaderboardBrevet, brevet, result, km): void {
    let findResult;
    if (brevet.distance === km) {
      findResult = leaderboardBrevet.find(x => x.name === result.name);
      if (!findResult) {
        leaderboardBrevet.push(result);
        findResult = leaderboardBrevet.find(x => x.name === result.name);
        findResult.route = brevet.title;
        findResult.startDate = brevet.startDate;
      } else if (+findResult.resultTime > +result.resultTime) {
        findResult.resultTime = result.resultTime;
        findResult.route = brevet.title;
        findResult.startDate = brevet.startDate;
      }
    }
  }

  statistics(distanceBrevet, brevet, result, km): void {
    if (brevet.distance === km && (distanceBrevet.resultTime === 0 || result.resultTime < distanceBrevet.resultTime)) {
      distanceBrevet.resultTime = result.resultTime;
      distanceBrevet.title = brevet.title;
      distanceBrevet.startDate = brevet.startDate;
    }
  }

  sortAndShort(resultsBrevet, resultsBrevetShort): void {
    resultsBrevet = resultsBrevet
      .sort((a, b) => a.resultTime - b.resultTime || a.name.localeCompare(b.name));
    let timeBrevet = 0;
    let i = 0;
    for (const item of resultsBrevet) {
      if (item.resultTime !== timeBrevet) {
        timeBrevet = item.resultTime;
        i++;
      }
      item.number = i;
      if (i < 6) {
        resultsBrevetShort.push(item);
      }
    }
  }

  endingWord(num): string {
    num = num % 10;
    let ending = '';
    if (num === 0 || (5 <= num && num <= 9)) {
      ending = 'ов';
    } else if (2 <= num && num <= 4) {
      ending = 'а';
    }
    return ending;
  }

  SR(data): number {
    const num = data[0] + data[1] + data[2] + data[3];
    let jData = 0;
    let jSR = 0;
    const arraySR = [0, 0, 0, 0];
    for (let i = 0; i < num; i++) {
      if (data[jData] !== 0 && jData >= jSR) {
        arraySR[jSR]++;
        data[jData]--;
        if (jSR !== 3) {
          jSR++;
        } else {
          jSR = 0;
        }
      }
      if (jData < jSR || data[jData] === 0 || jSR === 0) {
        if (jData !== 3) {
          jData++;
        } else {
          jData = 0;
        }
      }
    }
    return arraySR.reduce((a, b) => Math.min(a, b));
  }

  multiplierLeaderboard(brevet, name): number {
    let result = 0;
    if (brevet.find(x => x.name === name)) {
      result = 1 / brevet.find(x => x.name === name).number;
    }
    return result;
  }

  dialogShowStatistics(statistics): void {
    this.dialog.open(DialogShowStatisticsComponent, {
      data: {statistics}
    });
  }

  dialogShowBrevets(brevets, km): void {
    this.dialog.open(DialogShowBrevetsComponent, {
      data: {brevets, km}
    });
  }

  dialogClose(year): void {
    this.router.navigate([year]).then();
  }
}

@Component({
  selector: 'app-dialog-show-statistics',
  templateUrl: './dialog-show-statistics.component.html',
  styleUrls: ['./statistics.component.css'],
})
export class DialogShowStatisticsComponent {
  constructor() {
  }
}

@Component({
  selector: 'app-dialog-show-brevets',
  templateUrl: './dialog-show-brevets.component.html',
  styleUrls: ['./statistics.component.css'],
})
export class DialogShowBrevetsComponent {
  constructor() {
  }
}
