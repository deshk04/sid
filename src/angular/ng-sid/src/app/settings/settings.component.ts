import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TdLoadingService } from '@covalent/core/loading';
import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';
import { PasswordService } from '../services/password.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  passwdForm: FormGroup;
  submitted = false;
  pwdChangeSuccess = false;

  constructor(
    private _formBuilder: FormBuilder,
    private _loadingService: TdLoadingService,
    private sidSnackbarComponent: SidSnackbarComponent,
    private passwordService: PasswordService
  ) {
    this.createForm();

  }

  ngOnInit(): void {
  }

  createForm() {
    this.passwdForm = this._formBuilder.group({
      curr_passwd: ['', Validators.required],
      new_passwd1: ['', [Validators.required, Validators.minLength(8)]],
      new_passwd2: ['', [Validators.required]]
    }, {
      // validator: this.validatePasswd()
    }
    );

  }

  validatePasswd() {
    if(this.passwdForm.controls['curr_passwd'].value.length < 6){
      this.sidSnackbarComponent.showMessage(
        'Invalid current password'
      );
      return false

    }
      if (this.passwdForm.controls['new_passwd1'].value !==
        this.passwdForm.controls['new_passwd2'].value) {
        this.sidSnackbarComponent.showMessage(
          'Passwords do not match'
        );
        return false
        // this.passwdForm.controls['new_passwd1'].setErrors({ mustMatch: true });

      }
      // else {
      //   this.passwdForm.controls['new_passwd1'].setErrors(null);
      // }
      return true
  }
  onPasswordChange() {
    if (this.passwdForm.invalid) {
      return;
  }

    if(this.validatePasswd()){
      this._loadingService.register('loadingsidjob');
      this.passwordService.changePasswd(this.passwdForm).subscribe(
        (result) => {
          if(result.status == 'ok'){
            this.sidSnackbarComponent.showMessage(
              result.message, true
            );
          }else{
            this.sidSnackbarComponent.showMessage(
              result.message);

          }
          this._loadingService.resolve('loadingsidjob');

        },
        (err) => {
          console.log(err);
          this._loadingService.resolve('loadingsidjob');
          this.sidSnackbarComponent.systemError();

        }
        );




  }

  }
}
