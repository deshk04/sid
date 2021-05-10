import { Component} from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { Router, ActivatedRoute  } from '@angular/router';

import { UserAuthService } from '../services/auth.service';
import { IUserProfile } from '../models/userprofile';

@Component({
  selector: 'logout',
  styleUrls: ['./logout.component.scss'],
  templateUrl: './logout.component.html',
})
export class LogoutComponent {

	userProfileRecord: IUserProfile;
	data = ''; // for future use
	message = 'You are logged off';

	constructor(private userAuthService: UserAuthService,
				) {
				userAuthService.logout();
	}
}
