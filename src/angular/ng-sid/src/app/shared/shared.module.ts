import { NgModule, } from '@angular/core';
import { CommonModule, } from '@angular/common';
import { FormsModule, ReactiveFormsModule, } from '@angular/forms';

import { CovalentDataTableModule } from '@covalent/core/data-table';
import { CovalentMediaModule } from '@covalent/core/media';
import { CovalentLoadingModule } from '@covalent/core/loading';
import { CovalentNotificationsModule } from '@covalent/core/notifications';
import { CovalentLayoutModule } from '@covalent/core/layout';
import { CovalentMenuModule } from '@covalent/core/menu';
import { CovalentPagingModule } from '@covalent/core/paging';
import { CovalentSearchModule } from '@covalent/core/search';
import { CovalentStepsModule } from '@covalent/core/steps';
import { CovalentCommonModule } from '@covalent/core/common';
import { CovalentDialogsModule } from '@covalent/core/dialogs';
import { CovalentExpansionPanelModule } from '@covalent/core/expansion-panel';
import { CovalentMessageModule } from '@covalent/core/message';
import { CovalentVirtualScrollModule } from '@covalent/core/virtual-scroll';
import { CovalentFileModule } from '@covalent/core/file';
import { CovalentBreadcrumbsModule } from '@covalent/core/breadcrumbs';
import { CovalentChipsModule } from '@covalent/core/chips';

import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatTabsModule } from '@angular/material/tabs';
import { MatSelectModule } from '@angular/material/select';
import { MatRadioModule } from '@angular/material/radio';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSliderModule } from '@angular/material/slider';
import { MatStepperModule } from '@angular/material/stepper';
import { MatTreeModule } from '@angular/material/tree';

const ANGULAR_MODULES: any[] = [
    FormsModule, ReactiveFormsModule,
];

const MATERIAL_MODULES: any[] = [
    MatButtonModule, MatCardModule, MatIconModule,
    MatListModule, MatMenuModule, MatTooltipModule,
    MatSlideToggleModule, MatInputModule, MatCheckboxModule,
    MatToolbarModule, MatSnackBarModule, MatSidenavModule,
    MatTabsModule, MatSelectModule, MatRadioModule, MatGridListModule,
    MatTableModule, MatFormFieldModule, MatDatepickerModule,
    MatNativeDateModule, MatSliderModule, MatStepperModule,
    MatTreeModule
];

const COVALENT_MODULES: any[] = [
    CovalentDataTableModule, CovalentMediaModule, CovalentLoadingModule,
    CovalentNotificationsModule, CovalentLayoutModule, CovalentMenuModule,
    CovalentPagingModule, CovalentSearchModule, CovalentStepsModule,
    CovalentCommonModule, CovalentDialogsModule, CovalentExpansionPanelModule,
    CovalentMessageModule, CovalentVirtualScrollModule, CovalentFileModule,
    CovalentBreadcrumbsModule, CovalentChipsModule
];


@NgModule({
    imports: [
        CommonModule,
        ANGULAR_MODULES,
        MATERIAL_MODULES,
        COVALENT_MODULES,
    ],
    declarations: [

    ],
    exports: [
        ANGULAR_MODULES,
        MATERIAL_MODULES,
        COVALENT_MODULES,
    ]
})
export class SharedModule { }
