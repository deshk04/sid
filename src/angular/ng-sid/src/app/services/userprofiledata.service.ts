import { Injectable } from '@angular/core';
import { IUserProfile } from '../models/userprofile';

import { BehaviorSubject } from 'rxjs';

/*******************************************************************************
    this is the storage area for userprofile
    if the value is changed then it is broadcasted to all subscriber
*******************************************************************************/

@Injectable()
export class UserProfileDataService {
    tempProfile: IUserProfile = { first_name: '', last_name: '', email_id: '' , role: null, photo: '', isLoggedIn: false};

    profileRecord: BehaviorSubject<IUserProfile> = new BehaviorSubject<IUserProfile>(this.tempProfile);
    constructor() { }

}
