import {Component, OnInit} from '@angular/core';
import * as L from 'leaflet/dist/leaflet';
import 'leaflet-routing-machine';
import {take} from 'rxjs/operators';
import {ActivatedRoute, Router} from '@angular/router';
import {BrevetsData, RoutesData} from '../shell/shell.component';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  brevetsData: BrevetsData[];
  brevet: BrevetsData;
  routesData: RoutesData[];
  route: RoutesData;
  legend = [];
  year: string;
  routeTitle: string;
  link = window.location.href;

  constructor(private activatedRoute: ActivatedRoute, private router: Router) {
  }

  ngOnInit(): any {
    document.getElementById('legend').style.display = 'none';
    document.getElementById('legend').style.height = (window.innerHeight - 74).toString() + 'px';
    this.brevetsData = this.activatedRoute.snapshot.data.brevetsResolver;
    this.routesData = this.activatedRoute.snapshot.data.routesResolver;
    this.legend = this.activatedRoute.snapshot.data.legendsResolver;
    this.activatedRoute.paramMap.pipe(take(1))
      .subscribe(data => this.year = data.get('year'));
    this.activatedRoute.paramMap.pipe(take(1))
      .subscribe(data => {
        this.routeTitle = data.get('routeTitle');
        for (const item of this.brevetsData) {
          if (item.route === this.routeTitle) {
            this.brevet = item;
          }
        }
        for (const item of this.routesData) {
          if (item.title === this.routeTitle) {
            this.route = item;
          }
        }
        if (!this.routeTitle || !this.brevet || !this.route) {
          this.router.navigate([this.year]).then();
        } else {
          this.routeBuilding();
        }
      });
  }

  routeBuilding(): void {
    const LeafIcon = L.Icon.extend({
      options: {
        iconSize: [30, 50],
        iconAnchor: [15, 50],
        popupAnchor: [0, -35]
      }
    });
    const startIcon = new LeafIcon({
      iconUrl: 'assets/start.png',
    });
    const checkIcon = new LeafIcon({
      iconUrl: 'assets/check.png',
    });
    const finishIcon = new LeafIcon({
      iconUrl: 'assets/finish.png',
    });
    const startfinishIcon = new LeafIcon({
      iconUrl: 'assets/startfinish.png',
    });
    const myMap = L.map('map').setView([54.9807598975244, 73.3729112148285], 5);
    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoib2F0c21va2UiLCJhIjoiY2tsczRxN3JxMGozaTJxbXBuZzhoemVheCJ9.AdBxZbwEnTho74mKnj2OLQ', {
      maxZoom: 18,
      tileSize: 512,
      zoomOffset: -1,
    }).addTo(myMap);
    const routeControl = L.Routing.control({
      router: L.Routing.mapbox('pk.eyJ1Ijoib2F0c21va2UiLCJhIjoiY2tsczRxN3JxMGozaTJxbXBuZzhoemVheCJ9.AdBxZbwEnTho74mKnj2OLQ'),
      language: 'ru',
      addWaypoints: false,
      draggableWaypoints: false,
      show: false,
      waypoints: this.route.wayPoints,
      createMarker() {
        return null;
      }
    }).addTo(myMap);
    const brevet = this.brevet;
    const route = this.route;
    const optionsDate = {
      hour: 'numeric',
      minute: 'numeric',
      day: 'numeric',
      month: 'numeric',
      year: 'numeric',
    };
    routeControl.on('routeselected', function(e) {
      const instructionsRoute = e.route.instructions;
      const selectRoute = [0];
      let distance = 0;
      let i = 1;
      for (const item of instructionsRoute) {
        distance = distance + item.distance;
        if (item.type === 'WaypointReached' || item.type === 'DestinationReached') {
          selectRoute[i] = distance;
          i++;
        }
      }

      function timing(startDate, startTime, distanceToCheckPoint, max, min, speed, time, route, numberWayPoints, typeTime): any {
        if (numberWayPoints === route.wayPoints.length - 1 && typeTime === 'close') {
          time = brevet.totalTime;
        } else {
          for (let j = 0; j < 6; j++) {
            time = time + Math.min(Math.max(distanceToCheckPoint - max[j], 0), min[j]) / speed[j];
          }
          time = time + 1 / 120;
        }
        const startTimeToNumber = Math.trunc(startTime) + ((startTime - Math.trunc(startTime)) * 100) / 60;
        let checkPointH = Math.trunc(time + startTimeToNumber);
        const checkPointM = Math.trunc(((time + startTimeToNumber) - checkPointH) * 60);
        let day = 0;
        while (checkPointH >= 24) {
          checkPointH = checkPointH - 24;
          day++;
        }
        const startDateSplit = startDate.split('.');
        const toStartDate = new Date(startDateSplit[2], startDateSplit[1], startDateSplit[0]);
        return new Date(toStartDate.getFullYear(), toStartDate.getMonth() - 1, toStartDate.getDate() + day, checkPointH, checkPointM);
      }

      function timeCheckPoint(brevet, distanceToCheckPoint, popupName, route, numberWayPoints): any {
        let max = [200, 400, 600, 1000, 1200, 1800];
        let min = [200, 200, 400, 200, 600, 200];
        let speed = [32, 30, 28, 26, 25, 24];
        let time = Math.min(distanceToCheckPoint, 200) / 34;
        let typeTime = 'open';
        const openResult =
          timing(brevet.startDate, brevet.startTime, distanceToCheckPoint, max, min, speed, time, route, numberWayPoints, typeTime);
        max = [60, 600, 1000, 1200, 1400, 1800];
        min = [540, 400, 200, 200, 400, 200];
        speed = [15, 1.428, 13.333, 11, 10, 9];
        time = 1 + Math.min(distanceToCheckPoint, 60) / 20;
        if (numberWayPoints === route.wayPoints.length - 1) {
          distanceToCheckPoint = brevet.distance;
        }
        typeTime = 'close';
        const closeResult =
          timing(brevet.startDate, brevet.startTime, distanceToCheckPoint, max, min, speed, time, route, numberWayPoints, typeTime);
        popupTitle = '<br>' + popupName + ': ' + distanceToCheckPoint + 'км'
          + '<br>Открытие: ' + openResult.toLocaleString('ru', optionsDate)
          + '<br>Закрытие: ' + closeResult.toLocaleString('ru', optionsDate);
        return popupTitle;
      }

      function popupNameCheckPoint(number, numberCheckPoint): any {
        let markerIcon = checkIcon;
        let markerName = 'КП' + numberCheckPoint;
        if (number === 0) {
          markerIcon = startIcon;
          markerName = 'Старт';
        }
        if (number === route.wayPoints.length - 1) {
          markerIcon = finishIcon;
          markerName = 'Финиш';
        }
        return {markerName, markerIcon};
      }

      const markers = [];
      let popupName;
      let popupTitle;
      let numberCheckPoint = 0;
      let f = 0;
      for (i = 0; i < route.wayPoints.length; i++) {
        if (route.wayPoints[i][2] === 1) {
          popupName = popupNameCheckPoint(i, numberCheckPoint);
          popupTitle = timeCheckPoint(brevet, Math.round(selectRoute[i] / 1000), popupName.markerName, route, i);
          markers[f] = [route.wayPoints[i], popupName.markerIcon, route.checkPoints[numberCheckPoint][0], popupTitle];
          let doubleCheckPoint = numberCheckPoint;
          for (let j = i + 1; j < route.wayPoints.length; j++) {
            if (route.wayPoints[j][2] === 1 || route.wayPoints[j][2] === 2) {
              doubleCheckPoint++;
            }
            if (route.wayPoints[i][0] === route.wayPoints[j][0] && route.wayPoints[i][1] === route.wayPoints[j][1]) {
              route.wayPoints[j][2] = 2;
              popupName = popupNameCheckPoint(j, doubleCheckPoint);
              popupTitle = timeCheckPoint(brevet, Math.round(selectRoute[j] / 1000), popupName.markerName, route, j);
              if (j === route.wayPoints.length - 1) {
                markers[f][1] = startfinishIcon;
              }
              markers[f][3] = markers[f][3] + '' + popupTitle;
            }
          }
          numberCheckPoint++;
          f++;
        }
        if (route.wayPoints[i][2] === 2) {
          numberCheckPoint++;
        }
      }
      for (const item of markers) {
        L.marker(item[0], {icon: item[1]}).addTo(myMap).bindPopup(item[2] + '' + item[3]);
      }
    });
  }

  onResize(event): any {
    document.getElementById('map').style.width = event.target.innerWidth + 'px';
    document.getElementById('map').style.height = (event.target.innerHeight - 64) + 'px';
    document.getElementById('legend').style.height = (event.target.innerHeight - 64) + 'px';
  }

  showLegend(): any {
    if (document.getElementById('legend').style.display === 'none') {
      document.getElementById('legend').style.display = 'block';
    } else {
      document.getElementById('legend').style.display = 'none';
    }
  }

  dialogClose(year): any {
    this.router.navigate([year]).then();
  }
}
