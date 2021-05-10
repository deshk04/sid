export interface IExplorer {
    name: string;
    type: string;
    folder: string;
    children?: IExplorer[];

}
export interface IExplorerTree {
    tree: Array<IExplorer>;
}
export interface IExplorerRecords {
    status: string;
    message: Array<string>;
    num_of_records: number;
    records: IExplorerTree;
}
