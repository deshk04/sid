"""
  Description:    awss3 service
"""

import os

# import boto3
from core.general import settings


class AwsS3Service():
    """
        The class responsiblities are:
            Tree structure
    """

    def __init__(self, *args, **kwargs):
        self.client = None
        self.s3client = None
        self.bucket_name = None
        self.s3_bucket = None
        self.user_id = None
        self.s3objects = []

    def setup(self):
        self.client = self.s3client.session.client('s3')

    def getallfiles(self):
        """
            get all file details
        """
        for s3_file in self.s3_bucket.objects.all():
            record = {
                's3_file': s3_file,
                'key': s3_file.key
            }
            self.s3objects.append(record)

    def fetchfilefromkey(self, filekey):
        """
            get file details
        """
        if not filekey:
            return None

        file_name = os.path.basename(str(filekey))
        fpath = self.get_downloadpath()
        dest_file = fpath + file_name
        try:
            self.s3_bucket.download_file(filekey, dest_file)
            return dest_file
        except Exception:
            return None

    def fetchfilefrompath(self, i_path, i_startswith, i_endswith=None):
        """
            get file details
        """
        if not i_startswith or not i_path:
            return None

        for s3_file in self.s3_bucket.objects.filter(Prefix=i_path):
            """
                check if filename match
            """
            file_name = os.path.basename(str(s3_file.key))
            if i_endswith:
                if file_name.startswith(i_startswith) and \
                        file_name.endswith(i_endswith):
                    """
                        file match's let's return
                    """
                    return self.fetchfilefromkey(s3_file.key)
            else:
                if file_name.startswith(i_startswith):
                    """
                        file match's let's return
                    """
                    return self.fetchfilefromkey(s3_file.key)

        return None

    def getTreeView(self):
        if not self.client:
            return {}
        output = self.list_folders_in_bucket('')
        output['name'] = self.bucket_name
        return output

    def list_folders_in_bucket(self, fpath):
        dfdict = {'name': fpath}
        dfdict['type'] = "directory"
        dfdict['folder'] = fpath
        dfdict['children'] = []
        subdirectories = self.list_subfolder_in_bucket(fpath)
        if subdirectories:
            for folder in subdirectories:
                newsubfold = self.list_folders_in_bucket(folder)
                if newsubfold:
                    newsubfold['name'] = os.path.basename(
                        newsubfold['name'].rstrip('/'))
                    dfdict['children'].append(newsubfold)
            if not dfdict['children']:
                return None
        else:
            """
                files
            """
            files = self.list_files_in_bucket(fpath)
            dfdict['children'] = files
        return dfdict

    def list_subfolder_in_bucket(self, spath):
        folders = []
        paginator = self.client.get_paginator('list_objects')
        iterator = paginator.paginate(
            Bucket=self.bucket_name,
            Prefix=spath, Delimiter='/',
            PaginationConfig={'PageSize': None})
        for response_data in iterator:
            prefixes = response_data.get('CommonPrefixes', [])
            for prefix in prefixes:
                prefix_name = prefix['Prefix']
                if prefix_name.endswith('/'):
                    folders.append(prefix_name)
        return folders

    def list_files_in_bucket(self, spath):
        files = []
        paginator = self.client.get_paginator('list_objects')
        iterator = paginator.paginate(
            Bucket=self.bucket_name,
            Prefix=spath, Delimiter='/',
            PaginationConfig={'PageSize': None})
        for response_data in iterator:
            prefixes = response_data.get('Contents', [])
            for prefix in prefixes:
                prefix_name = prefix['Key']
                if not prefix_name.endswith('/'):
                    fdict = {'name': os.path.basename(prefix_name)}
                    fdict['type'] = 'file'
                    files.append(fdict)

        return files

    def get_downloadpath(self):
        """
            find the download path
        """
        if not self.user_id:
            self.user_id = settings.SID_ADMIN

        path = settings.DOCUMENT_PATH + str(self.user_id) + '/'
        if not os.path.isdir(path):
            os.mkdir(path)

        return path
