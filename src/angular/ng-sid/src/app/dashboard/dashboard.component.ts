import { Component, OnInit } from '@angular/core';
import { IUserProfile } from '../models/userprofile';

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  userProfileStatus = false;
  userProfileRecord: IUserProfile;
  userLoggedStatus = false;

  constructor(
  ) {

  }

  ngOnInit() {
  }

}
