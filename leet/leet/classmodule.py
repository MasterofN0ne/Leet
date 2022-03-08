import sys
import gspread
from google.oauth2.service_account import Credentials
import argparse
import pickle
import datetime 
from .Google import Create_Service

class SheetOps:

    def __init__(self):
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.API_NAME = 'drive'
        self.API_VERSION = 'v3'
        
        self.SCOPES = [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/drive.file',
                'https://www.googleapis.com/auth/spreadsheets'
            ]
        self.service = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        
        self.credentials = Credentials.from_service_account_file(
                    filename='service_account.json',
                    scopes=self.SCOPES
                )

        self.gc = gspread.authorize(self.credentials)
        self.args_list = []

        self.parser = argparse.ArgumentParser()

        self.subparser = self.parser.add_subparsers(dest="command")

        self.new = self.subparser.add_parser("new", help="Create new spreadsheet")
        self.init = self.subparser.add_parser("init", help="Initialize objects")
        self.commit = self.subparser.add_parser("commit", help="Commit changes")
        self.push = self.subparser.add_parser("push", help="Push changes")
        self.folder = self.subparser.add_parser('folder', help="Create a drive folder")

        self.folder.add_argument('-f', '--folder', metavar='', type=str, required=True, help='Specify folder name')
        self.new.add_argument('-n', '--name', metavar='', type=str, required=True, help='Name of spreadsheet')
        self.new.add_argument('-dir', '--directory', metavar='', type=str, required=False, help='Directory Name')
        self.init.add_argument('-q', '--question', metavar="", type=str, required=True, help="Leetcode Question")
        self.init.add_argument('-t', '--time', metavar="", type=str, required=True, help="Time spent on question")
        self.init.add_argument('-f', '--fail', metavar="", type=bool, required=True, help="Failed or not")
        self.init.add_argument('-qt', '--tag', metavar="", type=str, required=True, help="Tag of the question")
        self.init.add_argument('-m', '--message', metavar="", type=str, required=True, help="Commit message")
        self.push.add_argument('-url', '--url', metavar="", type=str, required=True, help="File url")
        self.args = self.parser.parse_args()

    def create_folder(self):
        url_temp = 'https://drive.google.com/drive/u/0/folders/'
        file_metadata = {
            'name': self.args.folder,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.service.files().create(body=file_metadata,
                                            fields='id').execute()

        file_url = url_temp + file['id']

        print(file['id'])

    def new_spreadsheet(self):
        #folder_id
        response = self.gc.create(title=self.args.name, folder_id=self.args.directory)
        sht = self.gc.open_by_key(response.id).sheet1

        self.gc.insert_permission(
            file_id=response.id,
            value='leetbot@leettracker-343018.iam.gserviceaccount.com',
            perm_type='user',
                role='writer'
        )

        self.gc.insert_permission(
                file_id=response.id,
                value=None,
                perm_type='anyone',
                role='writer'
            )

        sht.insert_row(values=(
                'LeetCode Question',
                'Time spent',
                'Commit Message',
                'isFailed',
                'date',
                'tag'
            ), 
            index=1)

        sample_url = 'https://docs.google.com/spreadsheets/d/'
        file_id = sample_url + response.id + '/edit#gid=0'

        print(file_id)

    def initializer(self):
        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y, %H:%M:%S")
        args_dict = {
            'Leetcode Question': self.args.question,
            'Time spent': self.args.time,
            'isFailed': self.args.fail,
            'Commit message': self.args.message,
            'Date': date,
            'Question Tag': self.args.tag
        }

        pickle_out = open("dict.pickle","wb")
        pickle.dump(args_dict, pickle_out)
        pickle_out.close


    def insert_values(self):
        """
            args_dict = {
            'Leetcode Question': self.args.question,
            'Time spent': self.args.time,
            'isFailed': self.args.fail,
            'Commit message': self.args.message,
            'Date': self.args.date,
            'Question Tag': self.args.tag
        }
        """
        sht = self.gc.open_by_url(self.args.url).sheet1
        pickle_in = open("dict.pickle","rb")
        example_dict = pickle.load(pickle_in)
        lst = [
            example_dict['Leetcode Question'],
            example_dict['Time spent'],
            example_dict['Commit message'],
            example_dict['isFailed'],
            example_dict['Date'],
            example_dict['Question Tag'],
        ]

        sht.insert_row(
            values= lst,
            index=2
        )

        print('File updated successfully')
    
    

