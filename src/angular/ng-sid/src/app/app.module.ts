import { NgModule, Type } from '@angular/core';
import { BrowserModule, Title } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule, HttpClientXsrfModule } from '@angular/common/http';
import { appRoutes, appRoutingProviders } from './app.routes';

import { AuthInterceptor } from './services/auth.interceptor';

import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { UserAuthService, AuthGuard } from './services/auth.service';
import { SharedModule } from './shared/shared.module';

import { AppComponent } from './app.component';
import { LayoutComponent } from './layout/layout.component';

import { MatButtonToggleModule } from '@angular/material/button-toggle';

import { MatDialogModule }  from '@angular/material/dialog';
import { MatAutocompleteModule }  from '@angular/material/autocomplete';
import { MatButtonModule }  from '@angular/material/button';
import { MAT_DATE_LOCALE }  from '@angular/material/core';
import { MAT_DATE_FORMATS }  from '@angular/material/core';
import { DateAdapter }  from '@angular/material/core';
import { SnotifyModule, SnotifyService, ToastDefaults } from 'ng-snotify';

import { MomentDateModule, MomentDateAdapter } from '@angular/material-moment-adapter';
import { DashboardComponent } from './dashboard/dashboard.component';
import { KeysPipe } from './pipes/keys';
// import { ProviderService } from './services/provider.service';
import { LoginComponent } from './login/login.component';
import { LogoutComponent } from './logout/logout.component';

//import { UserProfileService } from './services/userprofile.service';
import { UserProfileDataService } from './services/userprofiledata.service';
import { SearchConnectionsComponent } from './connections/searchconnections/searchconnections.component';
import { JobsComponent } from './jobs/jobs.component';
import { SettingsComponent } from './settings/settings.component';
import { NewconnectionComponent } from './connections/newconnection/newconnection.component';
import { SalesforceComponent } from './connections/salesforce/salesforce.component';
import { Awss3Component } from './connections/awss3/awss3.component';
import { JoblogsComponent } from './joblogs/joblogs.component';
import { SchedulesComponent } from './schedules/schedules.component';
import { SchedulelistComponent } from './schedules/schedulelist/schedulelist.component';
import { SchedulerecordComponent } from './schedules/schedulerecord/schedulerecord.component';

import { DimensionDataService } from './data/dimensiondata.service';
import { DimensionsComponent } from './dimensions/dimensions.component';
import { JobslistComponent } from './jobs/jobslist/jobslist.component';
import { DimensionsService } from './services/dimensions.service';
import { JobsService } from './services/jobs.service';
import { ConnectionlistComponent } from './connections/connectionlist/connectionlist.component';
import { ExplorerComponent } from './explorer/explorer.component';
import { S3explorerComponent } from './explorer/s3explorer/s3explorer.component';
import { SourceselectorComponent } from './jobs/editjob/sourceselector/sourceselector.component';
import { DocumentService } from './services/document.service';
import { DestselectorComponent } from './jobs/editjob/destselector/destselector.component';
import { SidSnackbarComponent } from './general/sidsnackbar/sidsnackbar.component';
import { JobdetailsComponent } from './jobs/jobdetails/jobdetails.component';
import { EditjobComponent } from './jobs/editjob/editjob.component';
import { PasswordService } from './services/password.service';
import { JoblogdetailsComponent } from './joblogs/joblogdetails/joblogdetails.component';
import { SchedulelogComponent } from './schedules/schedulelog/schedulelog.component';
import { SalesforceService } from './services/salesforce.service';
import { MapselectorComponent } from './jobs/editjob/mapselector/mapselector.component';
import { EditscheduleComponent } from './schedules/editschedule/editschedule.component';
import { QueryComponent } from './query/query.component';
import { SalesforcequeryComponent } from './query/salesforcequery/salesforcequery.component';


export const MY_FORMATS = {
    parse: {
      dateInput: 'DD/MM/YYYY',
    },
    display: {
      dateInput: 'DD/MM/YYYY',
      monthYearLabel: 'MM YYYY',
      dateA11yLabel: 'DD/MM/YYYY',
      monthYearA11yLabel: 'MM YYYY',
    },
  };

@NgModule({
    declarations: [
        AppComponent,
        LayoutComponent,
        DashboardComponent,
        KeysPipe,
        LoginComponent,
        LogoutComponent,
        SearchConnectionsComponent,
        JobsComponent,
        SettingsComponent,
        NewconnectionComponent,
        SalesforceComponent,
        Awss3Component,
        JoblogsComponent,
        SchedulesComponent,
        SchedulelistComponent,
        SchedulerecordComponent,
        DimensionsComponent,
        JobslistComponent,
        ConnectionlistComponent,
        ExplorerComponent,
        S3explorerComponent,
        SourceselectorComponent,
        DestselectorComponent,
        SidSnackbarComponent,
        JobdetailsComponent,
        EditjobComponent,
        JoblogdetailsComponent,
        SchedulelogComponent,
        MapselectorComponent,
        EditscheduleComponent,
        QueryComponent,
        SalesforcequeryComponent,
    ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        SharedModule,
        HttpClientModule,
        HttpClientXsrfModule.withOptions({
            cookieName: 'csrftoken',
            headerName: 'X-CSRFToken',
        }),
        appRoutes,
        MatButtonToggleModule,
        MatButtonModule,
        FormsModule,
        // new adds
        MatDialogModule,
        MatAutocompleteModule,
        CommonModule,
        SnotifyModule,
    ],
    providers: [
      UserAuthService,
      AuthGuard,
      {
        provide: HTTP_INTERCEPTORS,
        useClass: AuthInterceptor,
        multi: true
      },
//      UserProfileService,
      UserProfileDataService,
      DimensionDataService,
      DimensionsService,
      JobsService,
      DocumentService,
      {provide: MAT_DATE_LOCALE, useValue: 'en-au'},
      {provide: DateAdapter, useClass: MomentDateAdapter, deps: [MAT_DATE_LOCALE]},
      {provide: MAT_DATE_FORMATS, useValue: MY_FORMATS},
      {provide: 'SnotifyToastConfig', useValue: ToastDefaults},
      SnotifyService,
      SidSnackbarComponent,
      PasswordService,
      SalesforceService
    ],
    entryComponents: [],
    exports: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
