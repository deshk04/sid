import { Component, EventEmitter, Input, OnInit, Output, ChangeDetectorRef } from '@angular/core';

import { Router } from '@angular/router';
import { TdLoadingService } from '@covalent/core/loading';
import { NestedTreeControl } from '@angular/cdk/tree';
import { MatTreeNestedDataSource } from '@angular/material/tree';
import { IExplorerRecords, IExplorer } from '../../models/explorer'
import { ExplorerService } from '../../services/explorer.service';
import {saveAs as importedSaveAs} from 'file-saver';

import { SidSnackbarComponent } from 'src/app/general/sidsnackbar/sidsnackbar.component';

@Component({
  selector: 's3explorer',
  templateUrl: './s3explorer.component.html',
  styleUrls: ['./s3explorer.component.css']
})
export class S3explorerComponent implements OnInit {
  treeControl = new NestedTreeControl<IExplorer>(node => node.children);
  dataSource = new MatTreeNestedDataSource<IExplorer>();
  breadcrums = [];
  fileclicked = false;
  selectedFile = '';
  selectedPath = '';

  @Input()
  conn_id: number;

  @Input()
  showdownload: boolean = true;

  @Output('file')
  select: EventEmitter<string> = new EventEmitter<string>();

  dataloaded = false;
  hasChild = (_: number, node: IExplorer) => !!node.children && node.children.length > 0;

  constructor(
    private _changeDetectorRef: ChangeDetectorRef,
    private _loadingService: TdLoadingService,
    private router: Router,
    private explorerService: ExplorerService,
    private sidSnackbarComponent: SidSnackbarComponent

  ) {
    this.getTree();

  }

  ngOnInit(): void {
    this.getTree();
  }

  getTree() {
    if (!this.conn_id) {
      return;
    }
    this._loadingService.register('loadingsids3');

    this.explorerService.getTreebyId(this.conn_id).subscribe(
      result => {
        this._loadingService.resolve('loadingsids3');
        this.dataSource.data = this._processData(result.records.tree);
        this.dataloaded = true;
        this._changeDetectorRef.detectChanges();

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsids3');
        this.sidSnackbarComponent.systemError();

      });
  }
  newJob() {
    this.select.emit('');
  }

  private _processData(data, parent = null) {
    data.forEach(item => {
      if (parent !== null) {
        item.parent = { name: parent.folder };
      } else {
        item.parent = null;
      }
      if (item.children) {
        this._processData(item.children, item);
      }
    });
    return data;
  }

  onLeafNodeClick(node: any): void {
    this.selectedFile = node.name;
    this.selectedPath = node.parent.name;
    this.fileclicked = true;
  }
  onParentNodeClick(node: IExplorer): void {
    this.breadcrums = node.folder.slice(0, -1).split('/');
    this.selectedFile = '';
    this.fileclicked = false;
  }
  downloadFile(){
    this._loadingService.register('loadingsids3');

    const filename = this.selectedPath.concat(this.selectedFile);
    this.explorerService.downloadS3file(this.conn_id, filename).subscribe(
      blob => {
        try{
          importedSaveAs(blob, this.selectedFile);
        }
        catch(e){
          this.sidSnackbarComponent.showMessage('Download Error');

        }
        finally{
          this._loadingService.resolve('loadingsids3');
        }

      },
      err => {
        console.log(err);
        this._loadingService.resolve('loadingsids3');
        this.sidSnackbarComponent.showMessage('Download Error');

      });
  }
  selectFile(){
    const filename = this.selectedPath.concat(this.selectedFile);
    this.select.emit(filename);

  }

}
