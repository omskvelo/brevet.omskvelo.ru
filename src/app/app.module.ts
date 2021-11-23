import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatNativeDateModule} from '@angular/material/core';
import {MatInputModule} from '@angular/material/input';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatCardModule} from '@angular/material/card';
import {HttpClientModule} from '@angular/common/http';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatDialogModule} from '@angular/material/dialog';
import {DialogShowResultComponent, MainComponent} from './main/main.component';
import {MapComponent} from './map/map.component';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {ResultComponent} from './result/result.component';
import {MatTableModule} from '@angular/material/table';
import {MatSortModule} from '@angular/material/sort';
import {TotalResultsComponent} from './total-results/total-results.component';
import {MatSelectModule} from '@angular/material/select';
import {RouterModule, Routes} from '@angular/router';
import {ShellComponent} from './shell/shell.component';
import {PropertiesResolver} from './properties.resolver';
import {DatePipe} from '@angular/common';
import {BrevetsResolver} from './brevets.resolver';
import {RoutesResolver} from './routes.resolver';
import {LegendsResolver} from './legends.resolver';
import {ClipboardModule} from '@angular/cdk/clipboard';
import {ResultsResolver} from './results.resolver';
import {DialogShowBrevetsComponent, DialogShowStatisticsComponent, StatisticsComponent} from './statistics/statistics.component';
import {MatGridListModule} from '@angular/material/grid-list';
import { FullStatisticsListComponent } from './full-statistics-list/full-statistics-list.component';
import { FullStatisticsBrevetsListComponent } from './full-statistics-brevets-list/full-statistics-brevets-list.component';

const routes: Routes = [
  {path: '', component: MainComponent},
  {
    path: ':year', component: MainComponent, resolve: {
      propertiesResolver: PropertiesResolver,
      brevetsResolver: BrevetsResolver,
      resultsResolver: ResultsResolver
    }
  },
  {
    path: ':year/total_results', component: TotalResultsComponent, resolve: {
      brevetsResolver: BrevetsResolver,
      resultsResolver: ResultsResolver,
      propertiesResolver: PropertiesResolver
    }
  },
  {
    path: ':year/statistics', component: StatisticsComponent, resolve: {
      brevetsResolver: BrevetsResolver,
      resultsResolver: ResultsResolver,
      propertiesResolver: PropertiesResolver
    }
  },
  {
    path: ':year/:routeTitle', component: MapComponent, resolve: {
      brevetsResolver: BrevetsResolver,
      routesResolver: RoutesResolver,
      legendsResolver: LegendsResolver
    }
  },
  {path: '**', component: MainComponent}
];

@NgModule({
  declarations: [
    MainComponent,
    MapComponent,
    DialogShowResultComponent,
    DialogShowStatisticsComponent,
    DialogShowBrevetsComponent,
    ResultComponent,
    TotalResultsComponent,
    ShellComponent,
    StatisticsComponent,
    FullStatisticsListComponent,
    FullStatisticsBrevetsListComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatInputModule,
    MatFormFieldModule,
    FormsModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatCardModule,
    HttpClientModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatSlideToggleModule,
    MatTableModule,
    MatSortModule,
    MatSelectModule,
    RouterModule.forRoot(routes),
    ClipboardModule,
    MatGridListModule
  ],
  entryComponents: [
    DialogShowResultComponent,
    DialogShowStatisticsComponent,
    DialogShowBrevetsComponent
  ],
  providers: [DatePipe, StatisticsComponent],
  bootstrap: [ShellComponent]
})
export class AppModule {
}
