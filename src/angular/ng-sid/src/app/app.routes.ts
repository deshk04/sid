import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './services/auth.service';

// import { LayoutComponent } from './layout/layout.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { LogoutComponent } from './logout/logout.component';
import { SearchConnectionsComponent } from './connections/searchconnections/searchconnections.component';
import { JobsComponent } from './jobs/jobs.component';
import { SettingsComponent } from './settings/settings.component';
import { NewconnectionComponent } from './connections/newconnection/newconnection.component';
import { JoblogsComponent } from './joblogs/joblogs.component';
import { SchedulesComponent } from './schedules/schedules.component';
import { ExplorerComponent } from './explorer/explorer.component';
import { JobdetailsComponent } from './jobs/jobdetails/jobdetails.component';
import { EditjobComponent } from './jobs/editjob/editjob.component';
import { JoblogdetailsComponent } from './joblogs/joblogdetails/joblogdetails.component';
import { SchedulerecordComponent } from './schedules/schedulerecord/schedulerecord.component';
import { EditscheduleComponent } from './schedules/editschedule/editschedule.component';
import { QueryComponent } from './query/query.component';

export const routes: Routes = [
    { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent},
    { path: 'logout', component: LogoutComponent},
    { path: 'connections', component: SearchConnectionsComponent, canActivate: [AuthGuard]},
    { path: 'jobs', component: JobsComponent, canActivate: [AuthGuard]},
    { path: 'jobdetails/:id', component: JobdetailsComponent, canActivate: [AuthGuard]},
    { path: 'editjob/:id/:type', component: EditjobComponent, canActivate: [AuthGuard]},

    { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard]},
    { path: 'newconnection', component: NewconnectionComponent, canActivate: [AuthGuard]},
    { path: 'joblogs', component: JoblogsComponent, canActivate: [AuthGuard]},
    { path: 'schedule', component: SchedulesComponent, canActivate: [AuthGuard]},
    { path: 'explorer', component: ExplorerComponent, canActivate: [AuthGuard]},
    { path: 'joblogdetails/:id', component: JoblogdetailsComponent, canActivate: [AuthGuard]},
    { path: 'scheduledetails/:id', component: SchedulerecordComponent, canActivate: [AuthGuard]},
    { path: 'editschedule/:id/:type', component: EditscheduleComponent, canActivate: [AuthGuard]},
    { path: 'query', component: QueryComponent, canActivate: [AuthGuard]},

];

export const appRoutingProviders: any[] = [

];

export const appRoutes: any = RouterModule.forRoot(routes, { useHash: true });
