import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { Router, ActivatedRoute } from '@angular/router';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms'; // new add
import { FormControl } from '@angular/forms';

import { TdLoadingService } from '@covalent/core/loading';

import { IUserInput } from '../models/userprofile';
import { UserAuthService } from '../services/auth.service';
import { map } from 'rxjs/operators';
//import { runInThisContext } from 'vm';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
    selector: 'app-login',
    styleUrls: ['./login.component.scss'],
    templateUrl: './login.component.html',
})
export class LoginComponent implements OnInit {
    authSuccess = false;
    errorMessage = false;
    username = '';
    message = 'Please login';
    userRecord: IUserInput = { username: '', password: '' };

    constructor(private userAuthService: UserAuthService,
        private _loadingService: TdLoadingService,
        private router: Router,
        private sidSnackbarComponent: SidSnackbarComponent

    ) {
        //this.fetchUserProfile();
    }

    ngOnInit() {

    }
    onSubmit() {
        // console.log(this.userRecord);

       this._loadingService.register('loadingauth');

        this.userAuthService.login(this.userRecord).subscribe(
            result => {
               // console.log(result);

                this._loadingService.resolve('loadingauth')

                if(this.userAuthService.isLoggedIn){
                    this.authSuccess=true;
                    this.router.navigate(['dashboard']);
                }
                else {
                    this.sidSnackbarComponent.showMessage('Invalid Username / Password');
                }

            },
            err => {
                this._loadingService.resolve('loadingauth');
                this.sidSnackbarComponent.showMessage('Invalid Username / Password');
            })

    }

}
